# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
This file is loaded automatically by the application at startup
It sets up the Toolkit context and prepares the engine to run.
"""

import os
import sys
import traceback


__author__ = "Diego Garcia Huerta"
__contact__ = "https://www.linkedin.com/in/diegogh/"


def display_error(msg, logger=None):
    if logger:
        logger.error("Shotgun Error | Harmony engine | %s " % msg)
    print("Shotgun Error | Harmony engine | %s " % msg)


def display_warning(msg, logger=None):
    if logger:
        logger.warning("Shotgun Warning | Harmony engine | %s " % msg)
    print("Shotgun Warning | Harmony engine | %s " % msg)


def display_info(msg, logger=None):
    if logger:
        logger.info("Shotgun Info | Harmony engine | %s " % msg)
    print("Shotgun Info | Harmony engine | %s " % msg)


def start_toolkit_classic():
    """
    Parse enviornment variables for an engine name and
    serialized Context to use to startup Toolkit and
    the tk-harmony engine and environment.
    """
    import sgtk

    logger = sgtk.LogManager.get_logger(__name__)

    logger.debug("Launching toolkit in classic mode.")

    # Get the name of the engine to start from the environement
    env_engine = os.environ.get("SGTK_ENGINE")
    if not env_engine:
        msg = "Shotgun: Missing required environment variable SGTK_ENGINE."
        display_error(msg, logger)
        return

    # Get the context load from the environment.
    env_context = os.environ.get("SGTK_CONTEXT")
    if not env_context:
        msg = "Shotgun: Missing required environment variable SGTK_CONTEXT."
        display_error(msg, logger)
        return
    try:
        # Deserialize the environment context
        context = sgtk.context.deserialize(env_context)
    except Exception as e:
        msg = (
            "Shotgun: Could not create context! Shotgun Pipeline Toolkit"
            " will be disabled. Details: %s" % e
        )
        etype, value, tb = sys.exc_info()
        msg += "".join(traceback.format_exception(etype, value, tb))
        display_error(msg, logger)
        return

    try:
        # Start up the toolkit engine from the environment data
        logger.debug(
            "Launching engine instance '%s' for context %s"
            % (env_engine, env_context)
        )
        engine = sgtk.platform.start_engine(env_engine, context.sgtk, context)
        logger.debug("Current engine '%s'" % sgtk.platform.current_engine())

    except Exception as e:
        msg = "Shotgun: Could not start engine. Details: %s" % e
        etype, value, tb = sys.exc_info()
        msg += "".join(traceback.format_exception(etype, value, tb))
        display_error(msg, logger)
        return


def start_toolkit():
    """
    Import Toolkit and start up a tk-harmony engine based on
    environment variables.
    """

    # Verify sgtk can be loaded.
    try:
        import sgtk
    except Exception as e:
        msg = "Shotgun: Could not import sgtk! Disabling for now: %s" % e
        display_error(msg)
        return

    # start up toolkit logging to file
    sgtk.LogManager().initialize_base_file_handler("tk-harmony")

    # Rely on the classic boostrapping method
    start_toolkit_classic()

    # Check if a file was specified to open and open it.
    file_to_open = os.environ.get("SGTK_FILE_TO_OPEN")
    if file_to_open:
        msg = "Shotgun: Opening '%s'..." % file_to_open
        display_info(msg)
        # TODO load a project if specified
        # .App.loadProject(file_to_open)

    # Clean up temp env variables.
    del_vars = ["SGTK_ENGINE", "SGTK_CONTEXT", "SGTK_FILE_TO_OPEN"]
    for var in del_vars:
        if var in os.environ:
            del os.environ[var]


def setup_environment():
    SGTK_HARMONY_MODULE_PATH = os.environ["SGTK_HARMONY_MODULE_PATH"]

    if SGTK_HARMONY_MODULE_PATH and SGTK_HARMONY_MODULE_PATH not in sys.path:
        sys.path.insert(0, SGTK_HARMONY_MODULE_PATH)


if __name__ == "__main__":
    # Fire up Toolkit and the environment engine when there's time.
    setup_environment()
    start_toolkit()
