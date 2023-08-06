import time
import grpc
import core_pb2 as core__pb2
from ta2_impl import TA2_Server

protocol_version = "2017.12.20"


stub_uris = {
    "uri1": {
        "error": False,
        "train_time": 5,
        "test_time": 1,
        "test_type": 3,
        "task_type": "classification",
        "metrics": { "accuracy": 0.85 }
    },
    "uri2": {
        "error": False,
        "train_time": 3,
        "test_time": 1,
        "test_type": 8,
        "task_type": "classification",
        "metrics": { "accuracy": 0.66, "mean_squared_error": 12.3 }
    },
    "uri3": {
        "error": True,
        "train_time": 2,
        "test_time": 1,
        "task_type": "classification"
    }
}

class CreatePipelineResult(object):

    def __init__(self, uri):
        self.uri = uri
        self.result = []

    def add_score(self, metric, value):
        self.result.append((metric, value))

    def scores(self):
        return (s for s in self.result)


class PipelineOptimizer(object):

    def __init__(self):
        self.session_id = None
        self.pipeline_id = None
        self.metrics = None
        self.id_counter = {}
        self.optimizer = TA2_Server()


    def make_id(self, prefix):
        try:
            self.id_counter[prefix] += 1
        except:
            self.id_counter[prefix] = 1
        return "%s:%d" % (prefix, self.id_counter[prefix])
    

    def create_pipeline(self,
                        session_id=None,   # string id created by start_session
                        data_uri=None,     # URI to dataset known to both TA2 and TA3
                        task_type=None,    # A value from core__pb2.TaskType (QUESTION: which supported?)
                        task_subtype=None, # A value from core__bp2.TaskSubtype
                        features=None,     # Stream of (resource_id, feature_name) tuples
                                           # QUESTION: What is the resource_id here?
                        targets=None,      # Stream of (resource_id, feature_name) tuples
                                           # QUESTION: What to do if multiple specified?
                        metrics=None):     # Stream of core_pb2.PerformanceMetric
        """
        Allocate a new pipeline, returning a string ID.
        For the moment:
           Assume only one running pipeline at any given time.
           Return None on error.
        """
        
        # Client is attempting to interact on an unknown session
        if session_id != self.session_id:
            print("Session IDs do not match: %s, %s" % (session_id, self.session_id))
            return None

        # Tell optimizer to get ready to train, checking for error conditions.
        self.metrics = metrics
        # Ideally, we'd covert the GRPC-specific values into something the optimizer understands
        # QUESTION: What's the right way to do that?
        success = self.optimizer.prepare_pipeline(data_uri, task_type, task_subtype, features, targets)
        if not success:
            return None

        print("Prepare data URI: %s" % self.optimizer.data_uri)

        # No error conditions.
        self.pipeline_id = self.make_id("pipeline")
        return self.pipeline_id


    def run_pipeline(self, pipeline_id):
        """
        Start a previously allocated pipeline identified by pipeline_id.
        Returns a CreatePipelineResult object.
        """
        if pipeline_id != self.pipeline_id:
            print("Pipeline IDs: %s, %s" % (pipeline_id, self.pipeline_id))
            return None

        print("Run data URI: %s" % self.optimizer.data_uri)

        result_uri = self.optimizer.run_pipeline()
        if result_uri is None:
            print("Optimizer returned a null result URI")
            return None

        result = CreatePipelineResult(result_uri)
        for metric in self.metrics:
            score = self.optimizer.compute_metric(result_uri, metric)
            result.add_score(metric, score)

        return result


    def export_pipeline(self, session_id, pipeline_id, exec_uri):
        if self.session_id != session_id or self.pipeline_id != pipeline_id:
            print("export_pipeline: %s/%s; %s/%s" 
                  % (self.session_id, session_id, self.pipeline_id, pipeline_id))
            return False
        success = self.optimizer.export_pipeline(exec_uri)
        return success


    def prepare_execution(self, session_id, pipeline_id, data_uri):
        """
        Just informing the optimizer that we're going to be asked to execute a pipeline.
        Returns True if successful, else False.
        """
        if self.session_id != session_id or self.pipeline_id != pipeline_id:
            print("prepare_execution: %s/%s; %s/%s" 
                  % (self.session_id, session_id, self.pipeline_id, pipeline_id))
            return False

        success = self.optimizer.prepare_execution(data_uri)
        return success


    def execute_pipeline(self, pipeline_id):
        """
        Run the pipeline requested previously.  The assumption made in the protocol
        is that results of this execution (predictions) will be stored in a data file
        somewhere, and a URI returned for that data file.  This function runs to completion
        and returns that URI.  If it fails for any reason, it should return None.
        """
        if self.pipeline_id != pipeline_id:
            return None

        result_uri = self.optimizer.execute()
        return result_uri


    def supported_protocol(self, version):
        """
        Boolean method returning whether the protocol version the client proposes to speak
        is supported.
        """
        return version == protocol_version


    def start_session(self):
        """
        Start a new session and return a new session ID (string).
        """
        # We only handle one session at a time for now
        if self.session_id is not None:
            return None

        self.session_id = self.make_id("session")
        return self.session_id


    def end_session(self, session_id):
        """
        End a previously started session.  Return True to signal success, else False
        """
        if self.session_id is None:
            return False
        if self.session_id != session_id:
            return False
        self.session_id = None

        self.optimizer.free_session_resources()

        return True

    
