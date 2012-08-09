
fromdb = connect("127.0.0.1:27017/tera")
todb = connect("140.247.106.249:27017/tera")

fromdb['warpedfull'].find().forEach( function(x){todb['aligned'].insert(x)});

print("Done");




