from flask import Flask, render_template, url_for, request, redirect, make_response
import uuid

app = Flask(__name__)

meetings = {}
messages = {}

@app.route('/', methods=['GET'])
def initial():
    return render_template('initial.html')

@app.route('/submit', methods=['POST'])
def submitForm():
    tempUuid = str(uuid.uuid4())
    meetingName = request.form.get('meeting-name')
    memberName = request.form.get('member-name')
    meetings.update({tempUuid: [meetingName, memberName]})
    res = make_response(redirect(url_for('join', tempUuid=tempUuid)))
    res.set_cookie(tempUuid, memberName)
    return res

@app.route('/<tempUuid>', methods=['GET', 'POST'])
def join(tempUuid):
    if request.method == 'GET':
        if tempUuid not in meetings.keys():
            return redirect(url_for('initial'))

        elif request.cookies.get(tempUuid) is None:
            meetingName = meetings.get(tempUuid)[0]
            return render_template('join.html', tempUuid=tempUuid, meetingName=meetingName)

        else:
            if request.cookies.get(tempUuid) not in meetings.get(tempUuid):
                meetings.get(tempUuid).append(request.cookies.get(tempUuid))
            memberName = request.cookies.get(tempUuid)
            meetingName = meetings.get(tempUuid)[0]
            meetingMember = meetings.get(tempUuid)[1:]
            message = messages.get(tempUuid)
            return render_template('meeting.html', meetingName=meetingName, meetingMember=meetingMember, 
                                   message=message, tempUuid=tempUuid, memberName=memberName)
    
    else:
        memberName = request.form.get('member-name')
        meetings[tempUuid].append(memberName)
        res = make_response(redirect(url_for('join', tempUuid=tempUuid)))
        res.set_cookie(tempUuid, memberName)
        return res

@app.route('/chat', methods=['POST'])
def chat():
    tempUuid = request.args.get('id')
    message = request.form.get('mes')
    username = request.cookies.get(tempUuid)
    if messages.get(tempUuid) is None:
        messages.update({tempUuid: [[username, message]]})
    else:
        messages.get(tempUuid).append([username, message])
    return redirect(url_for('join', tempUuid=tempUuid))

@app.route('/leave', methods=['GET'])
def leave():
    tempUuid = request.args.get('id')
    memberName = request.cookies.get(tempUuid)
    meetings[tempUuid].remove(memberName)
    return redirect(url_for('initial'))

if __name__ == '__main__':
    
    app.run(debug=True)
