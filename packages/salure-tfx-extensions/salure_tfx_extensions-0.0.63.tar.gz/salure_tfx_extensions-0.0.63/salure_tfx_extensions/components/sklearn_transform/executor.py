"""Executor for the SKLearnTransform component"""

import os
import importlib.machinery
import joblib
import absl
import apache_beam as beam
import tensorflow as tf
from types import ModuleType
from typing import Any, Dict, List, Text, Tuple, Callable
from tfx import types
from tfx.components.base import base_executor
from tfx.types import artifact_utils
from tfx.utils import io_utils
from tfx.utils import path_utils
from tfx_bsl.tfxio import tf_example_record
from salure_tfx_extensions.utils import example_parsing_utils
from sklearn.pipeline import Pipeline

EXAMPLES_KEY = 'examples'
_DEFAULT_PIPELINE_NAME = 'preprocessing_pipeline'
_TELEMETRY_DESCRIPTORS = ['SKLearnTransform']


class Executor(base_executor.BaseExecutor):
    """Executor for the SKLearnTransform Component

    Takes in examples, and fits a transform pipeline, which it reads from a module file
    """

    def Do(self, input_dict: Dict[Text, List[types.Artifact]],
           output_dict: Dict[Text, List[types.Artifact]],
           exec_properties: Dict[Text, Any]) -> None:
        """
        Args:
          input_dict:
            - examples: Examples used for training, must include 'train' and 'eval' splits
          output_dict:
            - transformed_examples: The input examples, but transformed
            - transform_pipeline: The fit SKLearn Pipeline, for input preprocessing
          exec_properties:
            - module_file: The path to a module file
            - pipeline_name: The name of the Pipeline object in the module file
        """

        self._log_startup(input_dict, output_dict, exec_properties)

        if 'examples' not in input_dict:
            raise ValueError('\'examples\' is missing in input dict')
        if 'module_file' not in exec_properties:
            raise ValueError('\'module_file\' is missing in exec_properties')
        if 'transformed_examples' not in output_dict:
            raise ValueError('\'transformed_examples\' is missing in output_dict')
        if 'transform_pipeline' not in output_dict:
            raise ValueError('\'transform_pipeline\' is missing in output_dict')

        pipeline_name = exec_properties['preprocessor_pipeline_name'] or _DEFAULT_PIPELINE_NAME
        preprocessing_pipeline = import_pipeline_from_source(exec_properties['module_file'], pipeline_name)

        if not len(input_dict[EXAMPLES_KEY]) == 1:
            raise ValueError('input_dict[{}] should contain only 1 artifact'.format(
                EXAMPLES_KEY))

        # for SKLearn, all input data is put in as pandas Dataframes

        artifact = input_dict[EXAMPLES_KEY][0]
        splits = artifact_utils.decode_split_names(artifact.split_names)

        train_uri, eval_uri = example_parsing_utils.get_train_and_eval_uris(artifact, splits)

        input_tfxio = tf_example_record.TFExampleRecord(
            file_pattern=train_uri,
            telemetry_descriptors=_TELEMETRY_DESCRIPTORS
        )

        with self._make_beam_pipeline() as pipeline:
            # # For loading in a pcollection of tf.Examples
            # training_data = (
            #         pipeline
            #         | 'ReadTrainingExamplesFromTFRecord' >> beam.io.ReadFromTFRecord(
            #             file_pattern=train_uri)
            #         | 'ParseTrainingExamples' >> beam.Map(tf.train.Example.FromString))

            # For loading in Apache arrow Record Batches and turning into a PyArrow Table
            training_data = (
                pipeline
                | 'Read Training Examples as RecordBatches' >> input_tfxio.BeamSource()
                | 'Training Record Batches to Table' >> beam.CombineGlobally(
                    example_parsing_utils.RecordBatchesToTable())
                | 'To Pandas Dataframe' >> beam.Map(lambda x: x.to_pandas()))

            # training_data_rows = (
            #     training_data
            #     | 'Training Example to rows' >> beam.Map(
            #         example_parsing_utils.example_to_list)
            #     | 'Aggregating training rows' >> beam.CombineGlobally(
            #         example_parsing_utils.CombineFeatureLists())
            #     | 'Rows to numpy' >> beam.Map(example_parsing_utils.to_numpy_ndarray))
            _ = (
                training_data | 'Log DataFrame Head' >> beam.Map(lambda x: absl.logging.info(x.head().to_string()))
            )

            preprocessor_pcoll = (
                training_data
                | 'Fit Preprocessor' >> beam.ParDo(FitPreprocessingPipeline(pipeline))
            )


def import_pipeline_from_source(source_path: Text, pipeline_name: Text) -> Pipeline:
    """Imports an SKLearn Pipeline object from a local source file"""

    try:
        loader = importlib.machinery.SourceFileLoader(
            fullname='user_module',
            path=source_path,
        )
        user_module = ModuleType(loader.name)
        loader.exec_module(user_module)
        return getattr(user_module, pipeline_name)
    except IOError:
        raise ImportError('{} in {} not found in import_func_from_source()'.format(
            pipeline_name, source_path))


class FitPreprocessingPipeline(beam.DoFn):
    def __init__(self, pipeline):
        self.pipeline = pipeline
        super(FitPreprocessingPipeline, self).__init__()

    def process(self, matrix, *args, **kwargs):
        self.pipeline.fit(matrix)
        return self.pipeline


class TransformUsingPipeline(beam.DoFn):
    """Returns preprocessed inputs"""
    # TODO

    def __init__(self, pipeline: Pipeline):
        self.pipeline = pipeline
        super(TransformUsingPipeline, self).__init__()

    def process(self, element, *args, **kwargs):
        pass
