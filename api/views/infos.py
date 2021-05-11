from flask import jsonify


def infos_view(version, job_url, commit_sha):
    return jsonify({
        "version": version,
        "job_url": job_url,
        "commit_sha": commit_sha
    })
