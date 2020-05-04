#!/usr/bin/env python3
# coding: utf-8
from typing import cast

from flask import Blueprint, Response, request
from flask.json import jsonify

from genpei.const import GET_STATUS_CODE, POST_STATUS_CODE
from genpei.run import (dump_wf_params, fork_run, prepare_exe_dir,
                        prepare_run_dir, set_state, validate_run_request,
                        validate_wf_type)
from genpei.type import RunRequest, ServiceInfo, State
from genpei.util import generate_run_id, read_service_info

app_bp = Blueprint("genpei", __name__)


@app_bp.route("/service-info", methods=["GET"])
def get_service_info() -> Response:
    """
    May include information related (but not limited to) the workflow
    descriptor formats, versions supported, the WES API versions supported,
    and information about general service availability.
    """
    res_body: ServiceInfo = read_service_info()
    response: Response = jsonify(res_body)
    response.status_code = GET_STATUS_CODE

    return response


@app_bp.route("/runs", methods=["GET"])
def get_runs() -> Response:
    """
    This list should be provided in a stable ordering. (The actual ordering is
    implementation dependent.) When paging through the list, the client should
    not make assumptions about live updates, but should assume the contents of
    the list reflect the workflow list at the moment that the first page is
    requested. To monitor a specific workflow run, use GetRunStatus or
    GetRunLog.
    """
    res_body = {"msg": "Get Runs"}
    response: Response = jsonify(res_body)
    response.status_code = GET_STATUS_CODE

    return response


@app_bp.route("/runs", methods=["POST"])
def post_runs() -> Response:
    """
    This endpoint creates a new workflow run and returns a `RunId` to monitor
    its progress.
    """
    run_request: RunRequest = cast(RunRequest, dict(request.form))
    validate_run_request(run_request)
    validate_wf_type(run_request["workflow_type"],
                     run_request["workflow_type_version"])
    run_id: str = generate_run_id()
    prepare_run_dir(run_id, run_request)
    dump_wf_params(run_id, run_request)
    prepare_exe_dir(run_id, request.files)
    set_state(run_id, State.QUEUED)
    fork_run(run_id, run_request)
    response: Response = jsonify({
        "run_id": run_id
    })
    response.status_code = POST_STATUS_CODE

    return response


@app_bp.route("/runs/<run_id>", methods=["GET"])
def get_runs_id(run_id: str) -> Response:
    """
    This endpoint provides detailed information about a given workflow run.
    The returned result has information about the outputs produced by this
    workflow (if available), a log object which allows the stderr and stdout
    to be retrieved, a log array so stderr/stdout for individual tasks can be
    retrieved, and the overall state of the workflow run (e.g. RUNNING, see
    the State section).
    """
    res_body = {"msg": "Get Runs ID"}
    response: Response = jsonify(res_body)
    response.status_code = GET_STATUS_CODE

    return response


@app_bp.route("/runs/<run_id>/cancel", methods=["POST"])
def post_runs_id_cancel(run_id: str) -> Response:
    """
    Cancel a running workflow.
    """
    res_body = {"msg": "Post Runs ID Cancel"}
    response: Response = jsonify(res_body)
    response.status_code = POST_STATUS_CODE

    return response


@app_bp.route("/runs/<run_id>/status", methods=["GET"])
def get_runs_id_status(run_id: str) -> Response:
    """
    This provides an abbreviated (and likely fast depending on implementation)
    status of the running workflow, returning a simple result with the overall
    state of the workflow run (e.g. RUNNING, see the State section).
    """
    res_body = {"msg": "Get Runs ID Status"}
    response: Response = jsonify(res_body)
    response.status_code = GET_STATUS_CODE

    return response