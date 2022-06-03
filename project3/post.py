from flask import Flask,jsonify,request
app=Flask(__name__)
languages=[{'name':'kirti'},{'name':'verma'},{'name':'soni'}]
@app.route('/',methods=['GET'])
def test():
    return jsonify({'message':'It works'})
@app.route('/lang',methods=['get'])
def returnAll():
    return jsonify({'language':languages})
@app.route('/lang/<string:name>',methods=['get'])
def returnOne(name):
    lang=[language for language in languages if language['name']==name]
    return jsonify({'language':lang[0]})
@app.route('/lang',methods=['POST'])
def addone():
    language={'name':request.json['name']}
    languages.append(language)
    return jsonify({'language':languages})
@app.route('/lang/<string:name>',methods=['PUT'])
def editone(name):
    lang=[language for language in languages if language['name']==name]
    lang[0]['name']=request.json['name']
    return jsonify({'language':lang[0]})
@app.route('/lang/<string:name>',methods=['DELETE'])
def removeone(name):
    lang=[language for language in languages if language['name']==name]
    languages.remove(lang[0])
    return jsonify({'language':languages})




if __name__== '__main__':
    app.run(debug=True,port=3000)