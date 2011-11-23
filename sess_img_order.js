i = 0
db.sessions.find().forEach( function(sess) { sess.images.forEach( function(img) { new_item = {'img':img, 'pos':i}; db.sessions.update( {'_id':sess._id}, {$push: {'images_new': new_item}} ); i+=1 } ) } )

db.sessions.find().forEach( function(sess) { db.sessions.update( {'_id':sess._id}, {$unset: {'images': 1}} ) } )
db.sessions.find().forEach( function(sess) { db.sessions.update( {'_id':sess._id}, {$rename: {'images_new': 'images'}} ) } )
