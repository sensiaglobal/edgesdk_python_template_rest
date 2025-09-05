"""registration.py

Function to handle the combination of static and dynamic registration.
"""

import os
import sys
import json
import logging
import tarfile
from http import HTTPStatus

# Local
from api import RestAPI
from api.hcc2_rest_enums import (
    TagCategory
)
from api.hcc2_rest_schema import (
    GeneralDataPoint, ConfigDataPoint,
    TagMetadata, TagUnityUI
)
from config import AppConfig, ExitCode
from utils import info_banner, DataPoints

# Logging
hcc2_logger = logging.getLogger(AppConfig.app_func_name)
hcc2_logger.propagate = False


class AppConfigFile:
    """Application TAR.GZ configuration file wrapper class."""
    metadata = None
    archive_path = None
    _is_initialized = False

    @classmethod
    def initialize(cls, archive_path):
        """Initialize."""
        cls.archive_path = archive_path
        cls._load_config_files()
        cls._is_initialized = True

    @classmethod
    def is_loaded(cls) -> bool:
        """Return True if a static TAR.GZ config file is loaded."""
        return cls._is_initialized

    @classmethod
    def _load_config_files(cls):
        """Load metadata.json from the application TAR.GZ config file."""
        with tarfile.open(cls.archive_path, "r:gz") as tar:
            try:
                metadata_file = tar.extractfile("metadata.json")
                if metadata_file:
                    cls.metadata = json.loads(metadata_file.read())
            except KeyError:
                cls.metadata = None

            try:
                params_file = tar.extractfile("parameters.json")
                if params_file:
                    cls.parameters = json.loads(params_file.read())
            except KeyError:
                cls.parameters = None

    @classmethod
    def generate_data_points_from_metadata(cls) -> list[GeneralDataPoint]:
        """Extract info on general data points from TAR.GZ metadata.json. 
        Instantiate GeneralDataPoints for each and return as list."""
        general_datapoints = []
        config_datapoints = []

        general_dict = cls.metadata.get('general', {})
        config_dict = cls.metadata.get('config', {})

        for topic, metadata in general_dict.items():
            tag_subclass = topic.split('.')[1] if '.' in topic else ""
            general_datapoints.append(
                GeneralDataPoint(
                    topic=topic,
                    tagSubClass=tag_subclass,
                    metadata=TagMetadata(
                        dataType=metadata.get('_datatype', ""),
                        unit=metadata.get('_unit', "NONE"),
                        min=metadata.get('_recommendedMin', ""),
                        max=metadata.get('_recommendedMax', ""),
                        noProtobuf=metadata.get('_noCache', False),
                        builtinEnums="",
                        isInput=metadata.get('_input', False),
                        isOutput=metadata.get('_output', False),
                        arraySize=metadata.get('_maxsize', 1)
                    ),
                    unityUI=TagUnityUI(
                        displayName=metadata.get('_displayName', ""),
                        shortDisplayName=metadata.get('_shortDisplayName', "")
                    )
                )
            )

        for topic, metadata in config_dict.items():
            param_key = topic[:-1] if topic.endswith(':') else topic
            default_val = cls.parameters.get(param_key, "")
            
            config_datapoints.append(
                ConfigDataPoint(
                    topic=topic,
                    defaultValue=default_val,
                    metadata=TagMetadata(
                        dataType=metadata.get('_datatype', ""),
                        unit=metadata.get('_unit', "NONE"),
                        min=metadata.get('_recommendedMin', ""),
                        max=metadata.get('_recommendedMax', ""),
                        noProtobuf=metadata.get('_noCache', False),
                        builtinEnums="",
                        isInput=metadata.get('_input', False),
                        isOutput=metadata.get('_output', False),
                        arraySize=metadata.get('_maxsize', 1)
                    ),
                    unityUI=TagUnityUI(
                        displayName=metadata.get('_displayName', ""),
                        shortDisplayName=metadata.get('_shortDisplayName', "")
                    )
                )
            )

        return general_datapoints, config_datapoints


def registration():
    """Register an application with the HCC2.
    
    If static registration is enabled,
      -  Attempt to open specified TAR.GZ.
      -  Create new blank app if file not found.
    
    If dynamic registration is enabled,
      -  Attempt to define all general data points into previosuly opened TAR.GZ or blank app
      -  Attempt to define all config data points into previosuly opened TAR.GZ or blank app

    If both registration types are disabled,
      -  Only a blank application is registered.
    """

    info_banner("Registration")
    hcc2_logger.info(f"Static : {AppConfig.app_reg_static_en}")
    hcc2_logger.info(f"Dynamic General : {AppConfig.app_reg_dynamic_general_en}")
    hcc2_logger.info(f"Dynamic Config : {AppConfig.app_reg_dynamic_config_en}")
    hcc2_rest = RestAPI(version=1)
    generated_data_points = [], []


    # Static Config
    # ======================================
    # Open existing static config TAR.GZ file
    if AppConfig.app_reg_static_en and (os.path.exists(AppConfig.app_reg_premade_targz)):
        hcc2_logger.info(f"Registering Existing TAR.GZ {AppConfig.app_reg_premade_targz}")
        response = hcc2_rest.open_app(AppConfig.app_func_name, AppConfig.app_reg_premade_targz)
        if response.status_code == HTTPStatus.CREATED:
            hcc2_logger.info(f'App Config Loaded {AppConfig.app_func_name}')

            # Generate dataclasses for TAR.GZ datapoints
            AppConfigFile.initialize(AppConfig.app_reg_premade_targz)
            generated_data_points = AppConfigFile.generate_data_points_from_metadata()

    # Create new blank application
    else:
        hcc2_logger.info("Creating New Blank Application")
        response = hcc2_rest.initialize_app(AppConfig.app_func_name)
        if response.status_code == HTTPStatus.CREATED:
            hcc2_logger.info(f'Empty App Initilized {AppConfig.app_func_name}')

    hcc2_logger.info("--------------------------------")
    hcc2_logger.info("Static Data Points")
    hcc2_logger.info("--------------------------------")

    hcc2_logger.info("General:")
    for dp in generated_data_points[0]:
        hcc2_logger.info(f" - {dp.fqn}")

    hcc2_logger.info("Config:")
    for dp in generated_data_points[1]:
        hcc2_logger.info(f" - {dp.fqn}")


    # Dynamic Config
    # ======================================
    # Register all general and config datapoints
    hcc2_logger.info("--------------------------------")
    hcc2_logger.info("Dynamic Data Points")
    hcc2_logger.info("--------------------------------")

    # Register dynamic general tags
    if AppConfig.app_reg_dynamic_general_en:
        response = hcc2_rest.create_datapoints(
            AppConfig.app_func_name,
            TagCategory.GENERAL,
            DataPoints.general_points)

        if response.ok:
            hcc2_logger.info("General:")
            for dp in DataPoints.general_points:
                hcc2_logger.info(f" - {dp.fqn}")

        else:
            hcc2_logger.error(f"General Tag Registration Error: {response.text}")

    # Register dynamic config tags
    if AppConfig.app_reg_dynamic_config_en:
        response = hcc2_rest.create_datapoints(
            AppConfig.app_func_name,
            TagCategory.CONFIG,
            DataPoints.config_points)

        if response.ok:
            hcc2_logger.info("Config:")
            for dp in DataPoints.config_points:
                hcc2_logger.info(f" - {dp.fqn}")

        else:
            hcc2_logger.error(f"Config Tag Registration Error: {response.text}")


    # Registration
    # ======================================
    response = hcc2_rest.register_app(
        AppConfig.app_func_name,
        is_complex_provisioned=AppConfig.provisioning_complex)

    if response.status_code == HTTPStatus.CREATED:
        hcc2_logger.info("--------------------------------")
        hcc2_logger.info("Registration complete")

        # Add static datapoints
        for dp in generated_data_points[0]:
            DataPoints.add_general(dp)

        for dp in generated_data_points[1]:
            DataPoints.add_config(dp)

    else:
        hcc2_logger.critical(f"Registration failed: {response.text}")
        sys.exit(ExitCode.REGISTRATION_FAILED)
