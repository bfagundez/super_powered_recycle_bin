from sprb import sprb
from flask import request, jsonify
from redis import Redis
from sprb.views import sf

@sprb.route('/get_bin_records/<object_name>')
def get_bin_records(object_name):
    sfq = sf.queryAll("select id, Name from "+object_name+" where isDeleted = true")
    recs = []
    if sfq.size > 0:
        for rec in sfq.records:
            rec_serialized = { x : rec.__getitem__(x) for x in rec.__keylist__ }
            rec_serialized['obj_type'] = object_name
            recs.append(rec_serialized)

    return json.dumps(recs)

@sprb.route('/get_archived_bin_records')
def get_archived_records(object_name):
    # return archived items
    return json.dumps(recs)

@sprb.route('/api/archive', methods = ['POST'])
def archiveItem():

    payload = {}
    payload["success"] = False

    redis_conn = Redis()

    object_to_store = {}
    object_to_store['kind'] = 'archived'
    object_to_store['data'] = { x:request.form[x] for x in request.form.keys() }
    redis_conn.set(request.form['Id'], object_to_store)

    if redis_conn.get(request.form['Id']):
        payload["success"] = True
    #redis_conn.persist(request.form['Id'])

    return jsonify(payload)


@sprb.route('/api/restore', methods = ['POST'])
def restoreItem():
    payload = {}
    payload["success"] = False

    undel = sf.undelete(request.form['Id'])

    if undel.success:
        payload["success"] = True

    return jsonify(payload)

