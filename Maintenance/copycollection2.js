
fromdb = connect("127.0.0.1:27017/tera")
todb = connect("127.0.0.1:27017/")

a = fromdb.getCollectionNames();

print('Copying from '+ collect);
fromdb[collect].find().forEach( function(x){todb[collect].insert(x)});

print("Done");




