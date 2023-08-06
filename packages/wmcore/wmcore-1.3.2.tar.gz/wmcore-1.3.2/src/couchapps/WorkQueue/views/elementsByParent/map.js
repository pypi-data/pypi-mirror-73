function(doc, site) {
  var ele = doc["WMCore.WorkQueue.DataStructs.WorkQueueElement.WorkQueueElement"];
  // Can't get multiple keys to work - use one for now
  //emit([ele["Status"], ele["RequestName"], doc._id, doc.timestamp, ele["ParentQueueId"]],
  if (ele) {
    emit(ele["ParentQueueId"], {'_id' : doc['_id']});
  }
}