db.images.find().forEach( function(img) {db.sessions.update( {'chapter_id': img.title} , { $set: {'chapter_id': img.title}, $addToSet: {'images': img._id} }, true, false)} )
db.sessions.find().forEach( function(sess) { db.sessions.update( {'_id':sess._id}, {$set: {'label': db.chapters.findOne({'_id': sess.chapter_id}).name}} ) } )
db.sessions.find().forEach( function(sess) { db.sessions.update( {'_id':sess._id}, {$set: {'name': db.chapters.findOne({'_id': sess.chapter_id}).name}} ) } )

db.images.update( {}, {$unset: {'title': 1} } )
db.sessions.update( {}, {$unset: {'chapter_id': 1} } )
db.chapters.drop()

