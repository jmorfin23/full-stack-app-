from app import app, db
from flask import request, jsonify
from app.models import Event



#set index route to return nothing so no eerror occurs
@app.route('/')
def index():
    return ''

#use postman to check if api's  work
#post  is sending information
#get is retrieving information

#headers?
@app.route('/api/save', methods=['POST'])
def save():
    try:
        #get headers first
        title = request.headers.get('title')
        day = request.headers.get('day')
        month = request.headers.get('month')
        year = request.headers.get('year')
        notes = request.headers.get('notes')

        #if any info is missing give back an error jsonify message
        if not day or not title or not month or not year or not notes:
            return jsonify({ 'error': 'Invalid parameters '})

        #all info is included, save the event
        event = Event(title=title, day=day, month=month, year=year, notes=notes)

        #add to db
        db.session.add(event)
        db.session.commit()

        return jsonify({ 'success': 'saved event' })
    except:
        return jsonify({ 'error': 'Errors #002: Could not save event' })
@app.route('/api/retrieve', methods=['GET'])
def retrieve():

    try:

        day = request.headers.get('day')
        month = request.headers.get('month')
        year = request.headers.get('year')

        #year is required day cannot be paired with year, otherwise return Errors
        if not year:
            return jsonify({ 'error': 'Error #003: Year parameter is required'})
        elif day and not month:
            return jsonify({ 'error': 'Error #004: Month is required with day'})
        elif year and not month and not day:
            #get events for the entire year
            results = Event.query.filter_by(year=year).all()
        elif year and month and not day:
            #get events for the month passed
            results = Event.query.filter_by(year=year, month=month).all()
        else:
            #get events for the specific day
            results = Event.query.filter_by(year=year, month=month, day=day).all()
            #if results is empty, then there are no events, return response

        if results == []:
            return jsonify({ 'success': 'No events scheduled'})

        #loop over results because it is an instance of Event, save information into new list and return
        parties = []

        for result in results:
            party = {
            'title': result.title,
            'day': result.day,
            'month': result.month,
            'year': result.year,
            'notes': result.notes,
            'event_id': result.event_id
            }

            parties.append(party)

        return jsonify({ 'success': {
        'success': 'Retrieved Events',
        'events': parties
        }})
    except:
        return jsonify({'Error': 'Something went wrong'})
        
@app.route('/api/delete', methods=['DELETE'])
def delete():

    try:
        event_id = request.headers.get('event_id')

        event = Event.query.filter_by(event_id=event_id).first()

        if not event:
            return jsonify({ 'success': 'event does not exist'})
        title = event.title

        db.session.delete(event)
        db.session.commit()

        return jsonify({ 'success': f'Event "{title}" deleted.' })
    except:
        return jsonify({'Error': 'Something went wrong'})
