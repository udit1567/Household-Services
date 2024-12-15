from flask import Flask, render_template, redirect, request, redirect, url_for , flash, send_file
from flask import current_app as app
from .models import *
import io
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


@app.route('/')
def index():
    return render_template('index.html')

# creating a route for combined login page for Customer/Professionals/Admin
@app.route("/login", methods= ['GET', 'POST'])
def login():
    if request.method == 'POST':
        u_name = request.form.get('user_name')
        pwd = request.form.get('pwd')
        this_customer = Customer.query.filter_by(username = u_name).first()
        this_professional = Professionals.query.filter_by(username = u_name).first()

        if this_customer :
            if this_customer.password == pwd:
                if this_customer.application_status != "Active" :
                    flash('Your account has been blocked by the Admin')
                    return redirect('/login')
                return redirect(f'/customer_dashboard/{this_customer.id}')
            else:
                flash('incorrect password')
                return redirect('/login')
            
        elif this_professional :
            if this_professional.application_status == "Blocked" :
                flash('Your account has been blocked by the Admin')
                return redirect('/login')            
            elif this_professional.password == pwd:
                if this_professional.application_status == "Pending" :
                    flash('Your application is pending. Please wait for Admin approval !')
                    return redirect('/login')
                if this_professional.application_status == "Rejected" :
                    flash('Your application is rejected by Admin.')
                    return redirect('/login')
                return redirect(f'/professional_dashboard/{this_professional.id}')
            else:
                flash('incorrect password')
                return redirect('/login')
            
        elif u_name == 'Admin' and pwd == '123':
            return redirect('/admin_dashboard')
        else:
            flash('Invalid username or password')
            return redirect('/login')
                        
    return render_template('login.html')


#---------------------------------------- Customer's - endpoints ----------------------------------------

#creating a route for customer registration
@app.route("/register_customer", methods= ['GET','POST'])
def register_customer():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        full_name = request.form['fullname']
        address = request.form['address']
        pincode = request.form['pincode']
        phone_no = request.form['phone_no']

        if Customer.query.filter_by(username = username).first():
            flash('Username already exists! Please login.')
            return redirect('/login')

        new_customer = Customer(
            username=username,
            password=pwd,
            phone_no=phone_no,
            fullname=full_name,
            address=address,
            pincode=pincode
        )

        db.session.add(new_customer)
        db.session.commit()
        flash('Signup successful! please log in!')
        return redirect('/login')

    
    return render_template('register_customer.html')

#creating a route for Customer Dashboard
@app.route('/customer_dashboard/<int:c_id>', methods=['GET','POST'])
def Customer_login(c_id):
    this_customer = Customer.query.get(c_id)
    Service = Services.query.all()
    R_Services = this_customer.service_requests #all requested services of this customer

    return render_template('Customer_dashboards_home.html', user = this_customer, R_Services = R_Services , Service=Service )

#creating a route for editing customer information
@app.route("/edit_cust_info/<int:C_id>", methods=['GET','POST'])
def Edit_User_Info(C_id):
    if request.method == 'POST':
        username = request.form['username']
        full_name = request.form['fullname']
        address = request.form['address']
        pincode = request.form['pincode']
        phone_no = request.form['phone_no']
        
        this_customer = Customer.query.get(C_id)

        this_customer.username = username
        this_customer.phone_no = phone_no
        this_customer.fullname = full_name
        this_customer.address = address
        this_customer.pincode = pincode
        
        db.session.commit()

        return redirect(f'/customer_dashboard/{C_id}')


@app.route("/looking_for/<int:s_id>/<int:c_id>", methods=["GET","POST"])
def looking_for(s_id,c_id):
    if request.method == 'GET':
        all_professionals = Professionals.query.filter_by(service_id=s_id, application_status="Approved").order_by(desc(Professionals.rating)).all()
        user = Customer.query.get(c_id)
        this_service = Services.query.get(s_id)
        R_Services = user.service_requests

        return render_template('Customer_dashboards_lf.html', Professionals = all_professionals , R_Services = R_Services, user = user,  ser_name= this_service.service_name)
    
#creating a route to request services from customers dashboard
@app.route('/request_service/<int:p_id>/<int:c_id>/<int:s_id>', methods=["POST","GET"])
def request_service(p_id, c_id,s_id):
    this_service = Services.query.get(s_id)
    new_request = Service_Req(
        professional_id = p_id,
        service_id = s_id,
        customer_id = c_id,
        date_of_request = datetime.now().strftime("%B %d, %Y")
    )
    db.session.add(new_request)
    db.session.commit()

    return redirect(f"/looking_for/{this_service.id}/{c_id}")

#careating a route to mark ongoing serfvice as completed and submiting the service remark 
@app.route('/service_remark/<int:s_request_id>/<int:c_id>', methods=["POST","GET"])
def close_cust_request(s_request_id,c_id):
    if request.method == 'POST' :
        rating = request.form['rating']
        remarks = request.form['remarks']

        this_request = Service_Req.query.get(s_request_id)
        this_request.service_status = "Completed"
        this_request.service_rating = rating
        this_request.customer_remarks = remarks
        this_request.date_of_completion = datetime.now().strftime("%B %d, %Y")
        db.session.commit()

        return redirect(f'/customer_dashboard/{c_id}')

#creating a route for searching available services for the customer using serive-name/pincode/address
@app.route("/customer_search_services/<int:c_id>", methods=["GET", "POST"])
def customer_search_services(c_id):
    if request.method == "POST":
        search_by = request.form["search-by"]
        if search_by == 'service name':
            search_term = request.form["search_term"].capitalize()
            this_service = Services.query.filter(Services.service_name.like(f"{search_term}%")).first()
            
            if this_service:
                all_professionals = Professionals.query.filter_by(service_id = this_service.id ,application_status ="Approved").order_by(desc(Professionals.rating)).all()
                return render_template("Customer_dashboards_search.html", professionals = all_professionals, banner = this_service.service_name, c_id = c_id)
            
        elif search_by == 'pincode':

            pincode = request.form["search_term"]
            all_professionals = Professionals.query.filter_by(pincode = pincode ,application_status ="Approved").order_by(desc(Professionals.rating)).all()
            return render_template("Customer_dashboards_search.html", professionals = all_professionals, banner = "Availabe", c_id = c_id)
        
        elif search_by == 'address':
            address = request.form["search_term"]
            all_professionals = Professionals.query.filter(Professionals.address.like(f"%{address}%")).filter_by(application_status ="Approved").order_by(desc(Professionals.rating)).all()
            return render_template("Customer_dashboards_search.html", professionals = all_professionals, banner = "Availabe", c_id = c_id)
    
    
    return render_template("Customer_dashboards_search.html", c_id = c_id)

#creating a route for customer summary dashboard
@app.route('/cust_summary_dash/<int:c_id>', methods=["GET", "POST"])
def customer_summary_dash(c_id):
    try:
        user = Customer.query.get(c_id)
        requested_count = Service_Req.query.filter_by(customer_id=c_id, service_status="Requested").count()
        completed_count = Service_Req.query.filter(Service_Req.customer_id == c_id,
                                                    Service_Req.service_status.in_(['Closed', 'Completed'])).count()
        rejected_count = Service_Req.query.filter_by(customer_id=c_id, service_status="Rejected").count()
        ongoing_count = Service_Req.query.filter_by(customer_id=c_id, service_status="Accepted").count()


        labels = ["Requested","Ongoing" ,"Completed", "Rejected"]
        counts = [requested_count,ongoing_count, completed_count, rejected_count]


        plt.figure(figsize=(8, 6))
        plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90,colors = ['skyblue', 'lightgreen', 'Orange','salmon'])
        plt.title("Service Requests Status - Pie Chart")
        plt.legend(labels, loc="lower right", title="Status")
        plt.savefig('static/pie_chart.png')
        plt.close()


        plt.figure(figsize=(8, 6))
        plt.bar(labels, counts, color=['skyblue', 'lightgreen', 'Orange','salmon'])
        plt.xlabel("Request Status")
        plt.ylabel("Number of Requests")
        plt.title("Service Requests Status")
        plt.savefig('static/bar_chart.png')
        plt.close()


        return render_template("Customer_dashboard_summary.html",user = user)
    
    except Exception as e:
        return render_template("Customer_dashboard_summary.html",user = user, error = e)



#---------------------------------------- Professional's - endpoints ----------------------------------------

#creating a route for service professional registration 
@app.route("/register_professional", methods= ['GET','POST'])
def register_professional():
    if request.method == 'POST':
        full_name = request.form['full_name']
        username = request.form['email']
        pwd = request.form['password']
        service_id = request.form['service_id']
        experience = request.form['experience']
        address = request.form['address']
        pincode = request.form['pincode']
        file = request.files['document']
        phone_no = request.form['phone_no']

        if Professionals.query.filter_by(username = username).first() :
            flash('Username already exists ! Please login.')
            return redirect('/login')
        
        service = Services.query.get(service_id)
        
        if file and file.filename.endswith('.pdf'):
            document_data = file.read()          
            new_user = Professionals(
                fullname=full_name,
                username=username,
                password=pwd,
                phone_no=phone_no,
                service_id=service_id,
                experience=experience,
                pdf_doc=document_data,
                pricing=service.service_bp,
                time_req=service.time_req,
                service_desc=service.service_desc,
                address=address,
                pincode=pincode
            )
            
            db.session.add(new_user)
            flash('Signup successful!')
            db.session.commit()
            
            return redirect('/login')
        else:
            flash('file must be a PDF')
            return redirect('/register_professional')
    service = Services.query.all() 
    
    return render_template('register_professional.html', service=service)

#creating a route for professional dashboard
@app.route('/professional_dashboard/<int:p_id>', methods=['GET','POST'])
def professional_login(p_id):
    this_professional = Professionals.query.get(p_id)
    R_Services = Service_Req.query.filter_by(professional_id = p_id, service_status='Requested').all()
    a_Services = Service_Req.query.filter_by(professional_id = p_id).filter(Service_Req.service_status.in_(['Accepted','Closed', 'Completed'])).all()

    return render_template('profess_dashboards_home.html', professional = this_professional, R_Services = R_Services, c_Services = a_Services)


#creating a route for accepting customer's service requests
@app.route('/accept_cust_request/<int:s_request_id>/<int:p_id>')
def accept_cust_request(s_request_id,p_id):
    this_request = Service_Req.query.get(s_request_id)
    this_request.service_status = "Accepted"
    db.session.commit()

    return redirect(f'/professional_dashboard/{p_id}')

#creating a route for rejecting customer's service requests
@app.route("/reject_cust_request/<int:req_id>/<int:p_id>",)
def delete_cust_request(req_id, p_id):
    this_request = Service_Req.query.get(req_id)
    this_request.service_status = "Rejected"
    db.session.commit()

    return redirect(f'/professional_dashboard/{p_id}')

#creating a route for reviewing of a completed service request by professional
@app.route('/professional_review/<int:req_id>',methods=["GET", "POST"])
def professional_review(req_id):

    if request.method == 'POST':
        this_request = Service_Req.query.get(req_id)
        all_ratings = Service_Req.query.with_entities(Service_Req.service_rating).filter(Service_Req.professional_id == this_request.professional_id).all()

        total_rating = 0
        count = 0

        for rating in all_ratings:
            if rating[0] is not None:
                total_rating += rating[0]
                count += 1
        average_rating = round(total_rating / count, 1) if count > 0 else 0

        this_professional = Professionals.query.get(this_request.professional_id)
        this_professional.rating = average_rating
        remark = request.form['remark']
        this_request.professional_remark = remark
        this_request.service_status = "Closed"
        db.session.commit()

        return redirect(f'/professional_dashboard/{this_request.professional_id}')
    

@app.route('/professional_review_from_search/<int:req_id>', methods=["GET", "POST"])
def professional_review_from_search(req_id):

    if request.method == 'POST':
        this_request = Service_Req.query.get(req_id)
        all_ratings = Service_Req.query.with_entities(Service_Req.service_rating).filter(Service_Req.professional_id == this_request.professional_id).all()

        total_rating = 0
        count = 0

        for rating in all_ratings:
            if rating[0] is not None:
                total_rating += rating[0]
                count += 1
        average_rating = round(total_rating / count, 1) if count > 0 else 0

        this_professional = Professionals.query.get(this_request.professional_id)
        this_professional.rating = average_rating
        remark = request.form['remark']
        this_request.professional_remark = remark
        this_request.service_status = "Closed"
        db.session.commit()
        
        return redirect(f'/professional_search_services/{this_request.professional_id}')
    
#creating a route for searching accepted/closed/completed service requests    
@app.route("/professional_search_services/<int:p_id>", methods=["GET", "POST"])
def professional_search_services(p_id):
    if request.method == "POST":
        search_by = request.form["search-by"]
        
        if search_by == 'start Date':
            date = request.form["search_term"]
            c_Services = Service_Req.query.filter_by(professional_id = p_id ,
                                                    date_of_request =  date 
                                                    ).filter(Service_Req.service_status.in_(['Accepted','Closed', 'Completed'])).all()
            return render_template("Profess_dashboards_search.html", c_Services = c_Services, p_id = p_id)
            
        elif search_by == 'pincode':
            pincode = request.form["search_term"]
            c_Services = Service_Req.query.join(Customer).filter(
                                                                Customer.pincode == pincode,
                                                                Service_Req.professional_id == p_id,
                                                                Service_Req.service_status.in_(['Accepted','Closed', 'Completed'])
                                                            ).all()
            return render_template("Profess_dashboards_search.html", c_Services = c_Services, p_id = p_id)
        
        elif search_by == 'address':
            address = request.form["search_term"]
            c_Services = Service_Req.query.join(Customer).filter(
                                                                Service_Req.professional_id == p_id,
                                                                Service_Req.service_status.in_(['Accepted', 'Closed', 'Completed']),
                                                                Customer.address.like(f"%{address}%")
                                                            ).all()
            return render_template("Profess_dashboards_search.html", c_Services = c_Services, p_id = p_id)
        
    return render_template("Profess_dashboards_search.html", p_id = p_id)

@app.route("/edit_pro_info/<int:p_id>", methods = ["GET", "POST"])
def edit_pro_info(p_id):
    if request.method == "POST":
        this_professional = Professionals.query.get(p_id)
        this_professional.fullname = request.form["fullname"]
        this_professional.phone_no = request.form["phone_no"]
        this_professional.username = request.form["username"]
        this_professional.address = request.form["address"]
        this_professional.pincode = request.form["pincode"]
        this_professional.pricing = request.form["pricing"]
        this_professional.time_req = request.form["time_req"]
        this_professional.service_desc = request.form["service_desc"]

        db.session.commit()
        return redirect(f'/professional_dashboard/{p_id}')


#creating a summary page for professionals
@app.route('/profes_summary_dash/<int:p_id>', methods=["GET", "POST"])
def profes_summary_dash(p_id):
    try:
        this_professional = Professionals.query.get(p_id)
        requested_count = Service_Req.query.filter_by(professional_id=p_id, service_status="Requested").count()
        completed_count = Service_Req.query.filter(Service_Req.professional_id == p_id,
                                                    Service_Req.service_status.in_(['Closed', 'Completed'])).count()
        ongoing_count = Service_Req.query.filter_by(professional_id=p_id, service_status="Accepted").count()
        rejected_count = Service_Req.query.filter_by(professional_id=p_id, service_status="Rejected").count()

        labels = ["Requested","Ongoing", "Completed", "Rejected"]
        counts = [requested_count,ongoing_count, completed_count, rejected_count]

        rating = this_professional.rating
        rating_data = [rating, 5 - rating]
        label_1 = [f"Customer satisfacion", "Remaining"]
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(rating_data, labels=label_1, autopct='%1.1f%%', startangle=90, colors=['gold', 'lightgray'])
        ax.axis('equal')
        plt.title(f"Your current Rating: {rating} star")
        plt.savefig('static/pie_chart.png')
        plt.close()


        plt.figure(figsize=(8, 6))
        plt.bar(labels, counts, color=['skyblue', 'lightgreen', 'salmon'])
        plt.xlabel("Request Status")
        plt.ylabel("Number of Requests")
        plt.title("Requested service Status")
        plt.savefig('static/bar_chart.png')
        plt.close()


        return render_template("Professsionals_dashboard_summary.html",Professional = this_professional, p_id = p_id)
    
    except Exception as e:

        return render_template("Professsionals_dashboard_summary.html",Professional = this_professional, p_id = p_id, error = e)


#---------------------------------------- Admins's - endpoints ----------------------------------------

#Creating a route for admin Dashboard
@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    services = Services.query.all()
    Service_R = Service_Req.query.all()
    professionals = Professionals.query.filter(
        Professionals.application_status.in_(["Pending", "Approved", "Rejected"])).order_by(Professionals.id.desc()).all()
    return render_template('Admin_home.html',services=services,Service_R=Service_R,professionals=professionals)

#creating a route for adding new services
@app.route('/add_services', methods=['POST', 'GET'])
def add_services():
    if request.method == 'POST':
        service_name = request.form['service_name']
        base_price = request.form['base_price']
        time_req = request.form['time_req']
        service_desc = request.form['service_desc']
        new_service = Services(
            service_name = service_name,
            service_bp = base_price,
            time_req = time_req,
            service_desc = service_desc    
        )
        db.session.add(new_service)
        db.session.commit()

        flash("Service added successfully")
        
        return redirect('/admin_dashboard')
    
#creating a route to edit an existing service
@app.route('/edit_service/<int:id>', methods=['POST','GET'])
def edit_service(id):
    if request.method == 'POST':
        my_service = Services.query.get(id)        
        my_service.service_name = request.form['service_name']
        my_service.service_bp = request.form['base_price']
        my_service.time_req = request.form['time_req']
        my_service.service_desc = request.form['service_desc']
        db.session.commit()
        flash("Service updated successfully")

        return redirect('/admin_dashboard')

#creating a route to delete an existing service
@app.route('/delete_service/<int:id>', methods=['POST','GET'])
def delete_service(id):
    my_service = Services.query.get(id)
    db.session.delete(my_service)    
    db.session.commit() 
    flash("Service deleted successfully")

    return redirect('/admin_dashboard')

#creating a route to load professionals document
@app.route('/professional_pdf/<int:professional_id>')
def professional_pdf(professional_id):
    professional = Professionals.query.get(professional_id)
    
    if professional and professional.pdf_doc:
        return send_file(
            io.BytesIO(professional.pdf_doc),
            as_attachment=False,
            download_name='professional_document.pdf',
            mimetype='application/pdf'
        )
    else:
        return redirect('/admin_dashboard')
    
#creating a route for deleting a professional request
@app.route('/delete_professional/<int:id>', methods=["POST","GET"])
def delete_professional(id):   
    this_professional = Professionals.query.get(id)
    db.session.delete(this_professional)
    db.session.commit()

    return redirect('/admin_dashboard')

#creating a route to approve professionals request
@app.route('/approve_professional/<int:id>', methods=["POST","GET"])
def approve_professional(id):
    this_professional = Professionals.query.get(id)
    this_professional.application_status = "Approved"
    db.session.commit()

    return redirect('/admin_dashboard')

#creating a route to reject professionals request
@app.route('/reject_professional/<int:id>', methods=["POST","GET"])
def reject_professional(id):
    this_professional = Professionals.query.get(id)
    this_professional.application_status = "Rejected"
    db.session.commit()

    return redirect('/admin_dashboard')

#creating a route for displaying the summary of the  platform
@app.route('/Admin_summary', methods=["POST","GET"])
def admin_summary():
    try:
        requested_count = Service_Req.query.filter_by(service_status="Requested").count()
        completed_count = Service_Req.query.filter(Service_Req.service_status.in_(['Closed', 'Completed'])).count()
        Ongoing_count = Service_Req.query.filter_by(service_status="Accepted").count()
        rejected_count = Service_Req.query.filter_by(service_status="Rejected").count()
        customers_count = Customer.query.count()
        professionals_count = Professionals.query.count()
        services = Services.query.all()
        labels_3 = []
        counts_3 = []

        for service in services:
            labels_3.append(service.service_name)
            counts_3.append(len(service.service_requests))
        

        labels_1 = ["Requested","Ongoing" ,"Completed", "Rejected"]
        counts_1 = [requested_count,Ongoing_count ,completed_count, rejected_count]

        labels_2 = ["Customers", "Professionals"]
        counts_2 = [customers_count, professionals_count]

        plt.figure(figsize=(8, 6))
        plt.pie(counts_1, labels=labels_1, autopct='%1.1f%%', startangle=90,colors = ['skyblue', 'lightgreen', 'Orange','salmon'])
        plt.title("Service Request Status")
        plt.legend(labels_1, loc="lower right", title="Status")
        plt.savefig('static/pie_chart.png')
        plt.close()

        plt.figure(figsize=(8, 6))
        plt.bar(labels_1, counts_1, color=['skyblue', 'lightgreen', 'Orange','salmon'])
        plt.xlabel("Request Status")
        plt.ylabel("Number of Requests")
        plt.title("Service Request Status")
        plt.savefig('static/bar_chart.png')
        plt.close()

        plt.figure(figsize=(8, 6))
        plt.bar(labels_2, counts_2, color=['lightblue', 'green'])
        plt.xlabel("Users")
        plt.ylabel("Number of active users")
        plt.title("Application user traffic")
        plt.savefig('static/bar_chart_traffic.png')
        plt.close()

        plt.figure(figsize=(8, 6))
        plt.bar(labels_3, counts_3)
        plt.xlabel("Services")
        plt.ylabel("Number of requests")
        plt.title("Service demand")
        plt.savefig('static/bar_chart_demand.png')
        plt.close()
        return render_template('Admin_summary_dashboard.html')
    
    except Exception as e:
        return render_template('Admin_summary_dashboard.html', error = e)

#creating a route for managing the application users
@app.route('/Admin_manage', methods=["POST","GET"])
def admin_manage():
    all_requests = Service_Req.query.filter_by(service_status="Closed").all()
    all_professional = Professionals.query.order_by(asc(Professionals.rating)).all()
    return render_template('Admin_manage_dash.html' ,professionals = all_professional, Requests = all_requests)

#creating a route to block a customer
@app.route('/Block_customer/<int:c_id>', methods=["POST"])
def Block_customer(c_id):
    this_customer = Customer.query.get(c_id)
    this_customer.application_status = "Blocked"
    db.session.commit()
    return redirect('/Admin_manage')

#creating a route to unblock a customer
@app.route('/Unblock_customer/<int:c_id>', methods=["POST"])
def Unlock_customer(c_id):
    this_customer = Customer.query.get(c_id)
    this_customer.application_status = "Active"
    db.session.commit()
    return redirect('/Admin_manage')

#creating a route to block a professional
@app.route('/Block_professional/<int:p_id>', methods=["POST"])
def Block_professional(p_id):
    this_professional = Professionals.query.get(p_id)
    this_professional.application_status = "Blocked"
    db.session.commit()
    return redirect('/Admin_manage')

#creating a route for unblocking a professional
@app.route('/Unblock_professional/<int:p_id>', methods=["POST"])
def Unlock_professional(p_id):
    this_professional = Professionals.query.get(p_id)
    this_professional.application_status = "Approved"
    db.session.commit()
    return redirect('/Admin_manage')

#creating a route for searching the services
@app.route('/Admin_search_services', methods=['GET','POST'])
def admin_search_services():
    if request.method == 'POST':
        search_by = request.form["search-by"]
        if search_by == 'service name':
                search_term = request.form["search_term"].capitalize()
                this_service = Services.query.filter(Services.service_name.like(f"{search_term}%")).first()
                if this_service:
                    all_req_services = Service_Req.query.filter_by(service_id = this_service.id).all()
                    return render_template("Admin_search_dash.html", Service_R = all_req_services)
        elif search_by == 'pincode':
            pincode = request.form["search_term"]
            all_req_services = Service_Req.query.join(Customer).filter(Customer.pincode == pincode,).all()
            return render_template("Admin_search_dash.html", Service_R = all_req_services)
        elif search_by == 'status':
                status = request.form["status"]
                all_req_services = Service_Req.query.filter_by(service_status = status).all()
                return render_template("Admin_search_dash.html", Service_R = all_req_services)
    return render_template("Admin_search_dash.html")   
