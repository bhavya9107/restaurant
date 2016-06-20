from flask import Flask,render_template,request,url_for,redirect

app=Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def first():
    output=""
    results = session.query(Restaurant.name,Restaurant.id).order_by(Restaurant.name).all()
    return render_template('homepage.html',results=results)

@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method=='GET':
        return render_template('deleterestaurant.html',restaurant=restaurant)
    if request.method=='POST':
        session.delete(restaurant)
        session.commit()
        return redirect(url_for('first'))
    
    


@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET','POST'])
def newMenuItem(restaurant_id):

	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course = request.form['course'], restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		return redirect(url_for('RestaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('newMenuItem.html', restaurant_id = restaurant_id,restaurant=restaurant)

@app.route('/restaurants/<int:restaurant_id>/<int:MenuID>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, MenuID):
    editedItem = session.query(MenuItem).filter_by(id = MenuID).one()
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
			editedItem.name = request.form['name']
        if request.form['description']:
			editedItem.description = request.form['description']
        if request.form['price']:
			editedItem.price = request.form['price']
        if request.form['course']:
			editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('RestaurantMenu', restaurant_id = restaurant_id))
    else:
		#USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
		return render_template('editmenuitem.html', restaurant_id = restaurant_id, MenuID = MenuID, item = editedItem,restaurant=restaurant)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete_item/',methods=['GET','POST'])

def deleteMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method=='GET':
        return render_template('deleteMenuItem.html',restaurant_id=restaurant_id,item=item)
    if request.method=='POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('RestaurantMenu', restaurant_id = restaurant_id))
    
        
    

@app.route('/restaurants/<int:restaurant_id>/')
def RestaurantMenu(restaurant_id):
    restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
    items=session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)
    
if __name__=='__main__':
    app.debug= True
    app.run() 

