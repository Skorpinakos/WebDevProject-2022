//Express.js
import express from 'express'
import { engine } from 'express-handlebars';
import * as model from './model/model.js';
import multer from 'multer';
import nodemailer from 'nodemailer';
const app = express(); //make app object
let port = process.env.PORT || '3000'; //set port
const router = express.Router(); //make a router object

const admin_keys = ['tsabras123', 'steve456'];

var transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: 'unireportuniversityofpatras@gmail.com',
    pass: 'zqegiddfnqglegok'
  }
});

const storage = multer.diskStorage({
    destination:(req,file,callback) =>{
        callback(null,'public/images') // path to store images
    },
    filename: (req, file, callback) => {
        //console.log(file)
        let filename = Date.now() + file.originalname.replaceAll(' ', '_');
        callback(null, filename)
    }
})

const imageFileFilter = (req, file, cb) =>{
    if(!file.originalname.match(/\.(jpg|jpeg|png|gif|PNG|JPG|JPEG|GIF|Png|Jpg|Jpeg|Gif|])$/)) { //If the file uploaded is not any of this file type

    // If error in file type, then attach this error to the request header
        req.fileValidationError = "You can upload only image files";
        return cb(null,false, req.fileValidationError);
    }
    cb(null, true)
};

const upload = multer({storage:storage, fileFilter: imageFileFilter});

app.set('view engine', 'handlebars');//Sets our app to use the handlebars engine
//Sets handlebars configurations 
app.use(express.static('public')); //make the 'public' directory public (users can acces it)
app.engine('hbs', engine({ extname: 'hbs' })); //for using 'hbs' file extension instead of 'handlebars'
app.set('view engine', 'hbs'); //set rendering engine the handlebars


// entities_properties = {

//     'Location': {"id": ['integer', True], "building": ['string', False], "coordinates_x": ['integer', False], "coordinates_y": ['integer', False]},

//     'Category': {"id": ['integer', True], "category_name": ['string', False, True], "urgency": ['integer', False], "mean_repair_time": ['time', False]},

//     'Technician': {"id": ['integer', True], "firstname": ['string', False], "lastname": ['string', False], "phone_number": ['string', False],
//                    "email": ['string', False], "specialization": ['string', False], "repairs": ['integer', False], "mean_repair_time": ['time', False]},

//     'Ticket': {"id": ['integer', True], "title": ['string', False], "description": ['text', False], "creation_date": ['date', False],
//                "closure_date": ['date', False], "state": ['string', False], "image_path": ['string', False], "contact_phone": ['string', False], "contact_email": ['string', False],
//                "locale": ['integer', False, 'Location', 'id'], "type": ['integer', False, 'Category', 'id']},

//     'Contract': {"id": ['integer', True], "key": ['string', False, True], "details": ['text', False], "date": ['date', False],
//                  "cost": ['float', False], "damage": ['integer', False, 'Ticket', 'id'], "repairman": ['integer', False, 'Technician', 'id']}

// }

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////// temp data before implementation of db
let x0=0;
let x_ratio=1;
let y0=0;
let y_ratio=1;
let buildings = [
    {'name' : 'Κτίριο Α'},
    {'name' : 'Κτίριο Β'},
    {'name' : 'Τρία συγκροτήματα αμφιθεάτρων της Σχολής Θετικών Επιστημών (ΑΘΕ)'},
    {'name' :'Κτίριο Τμήματος Φυσικής'},
    {'name' :'Κτίριο Τμήματος Χημείας'},
    {'name' :'Κτίριο Μηχανικών Ηλεκτρονικών Υπολογιστών και Πληροφορικής'},
    {'name' :'Κτίριο Τμήματος Ηλεκτρολόγων Μηχανικών και Τεχνολογίας Υπολογιστών'},
    {'name' :'Κτίριο Τμήματος Μηχανολόγων και Αεροναυπηγών Μηχανικών'},
    {'name' :'Κτίριο Τμήματος Πολιτικών Μηχανικών'},
    {'name' :'Κτίριο Επιστημών της Εκπαίδευσης και Κοινωνικής Εργασίας'},
    {'name' :'Κτίριο Τμήματος Χημικών Μηχανικών'},
    {'name' :'Κτίριο Τμήματος Βιολογίας'},
    {'name' :'Κτίριο Τμήματος Γεωλογίας'},
    {'name' :'Κτίριο Τμήματος Μαθηματικών'},
    {'name' :'Κτίριο Προκλινικών Λειτουργιών του Τμήματος Ιατρικής'},
    {'name' :'Κτιριακό συγκρότημα Κλινικών Λειτουργιών του Τμήματος της Ιατρικής'},
    {'name' :'Συγκρότημα Προκατασκευασμένων Κτιρίων'},
    {'name' :'Κτίριο Κεντρικής Βιβλιοθήκης και Κέντρου Πληροφόρησης'},
    {'name' :'Κτίριο Συνεδριακού και Πολιτιστικού Κέντρου του Πανεπιστημίου'},
    {'name' :'Λοιπές εγκαταστάσεις'},
    {'name' :'Φοιτητική Εστία'},
    {'name' :'Γραφεία του Πανεπιστημίου'},
    {'name' :'Αθλητικό κέντρο και γήπεδα'},
    {'name' :'Πανεπιστημιακό Γυμναστήριο'},
    {'name' :'Μουσείο Επιστημών και Τεχνολογίας'},
    {'name' :'Ραδιοφωνικός Σταθμός “UPfm”'},
    {'name' :'Συγκρότημα Προτύπων Πειραματικών Σχολείων του Πανεπιστημίου Πατρών “Ε. Παπανούτσος”'},
    {'name' :'Κέντρο Επιμόρφωσης και Διά Βίου Μάθησης (Κ.Ε.ΔΙ.ΒΙ.Μ.)'},
    {'name' :'Πανεπιστημιακό Γενικό Νοσοκομείο Πατρών'}
]

let categories = [
    {'name' : 'Ηλεκτρολογικά'},
    {'name' : 'Μηχανολογικά'},
    {'name' : 'Υδραυλικά'},
    {'name' : 'Οικοδομικά'}

]

let states =[
    {'name':'Υπό επεξεργασία'},
    {'name':'Ανοιχτή'},
    {'name':'Υπό επισκευή'},
    {'name':'Κλειστή'}
]

///////////////////////////////////////////////////////////////////////////////////////////////////////////////// backend functions
let give_home_page = function(req,res){
    //Serves the main page
    let displayedRecents = 6;
    model.getRecents(displayedRecents, (err, rows) => {   /////QUERY DONE//////////////////////////////////////////////////
        if (err){
          console.log(err.message);
        } 
        //console.log('Recents', rows)
        res.render('home_page', {layout : 'layout', recent_highlights:rows });
      });
};


let return_open_failures = function(req,res){
    //rest api command, Serves list of open failures that looks like [{'id':1,'x':100,'y',200},{'id':1,'x':700,'y',400},...], it is inside a json file under the name 'open_failures'
    let draw_limit=100;
    // here add query to db for retrieving list of failures that are currently unfixed and cast it to a list like this [{'id':1,'x':100,'y',200},{'id':1,'x':700,'y',400},...] named open_failures DONE////////////////////////////////
    model.get_open_failures_coords(draw_limit, (err, rows) => {   
        if (err){
          console.log(err.message);
        } 
        res.json({'open_failures':rows});
        //console.log(rows)
      });
    

};


let give_history_page = function(req,res){

    let information='Βλάβες με χρονολογική σειρά'
    // here add query for db that return the 6 all failures in chronological order DONE/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    let display_count= 30;
    model.getRecents(display_count, (err, rows) => {   
        if (err){
          console.log(err.message);
        } 
        //console.log('Recents', rows)
        res.render('history', {layout : 'layout',search_results:rows,information:information});
      });
    
};

let give_result_page = function(req,res){
    let search_text=req.query['input_text'];
    let information='Αποτελέσματα αναζήτησης'
    //console.log(search_text);
    // here add query for db that return the search results instead of the folllowing line, search results based on the 'search_text' variable DONE////////////////////////////////
    let display_count = 30;
    model.get_search_results(display_count,search_text, (err, rows) => {   
        if (err){
          console.log(err.message);
        } 
        //console.log('Recents', rows)
        res.render('history', {layout : 'layout',search_results:rows,information:information});
      });
};

let give_contractor_login_page = function(req,res){

    let error={'e_type':'','message':''};
    res.render('contractor_login', {layout : 'layout', error:error});

};

let give_contractor_page = function(req,res){
    let key=parseInt(req.query['input_text']);
    //console.log(serial_text);
    //check if serial number exists in contract table and insert the coresponding contracts info in contract_info bellow
    model.get_report_from_key(key, (err, rows) => {   
        console.log(key,rows)
        if (err){
          console.log(err.message);
        } 
        if (rows.length == 0){
            let error={'e_type':'undefined','message':'Το κλειδί σας δεν αντιστοιχεί σε κάποια αναφορά'};
            res.render('contractor_login', {layout : 'layout',error:error});

          } 
        else{
          let info_to_pass={};
          Object.assign(info_to_pass,rows[0]);
          info_to_pass['coords_to_show_x']=(info_to_pass['coordinates_x']*x_ratio+x0);
          info_to_pass['coords_to_show_y']=(info_to_pass['coordinates_y']*y_ratio+y0);
          info_to_pass['key'] = key;
          res.render('contractor_page', {layout : 'layout',failure_info:info_to_pass, buildings : buildings, categories : categories});
        }
      });    // fed ton an #each helper), we can use #
      
};

let give_admin_login_page = function(req,res){

    let error={'e_type':'','message':''};
    res.render('admin_login', {layout : 'layout', error:error});

};

let give_admin_history = function(req,res){
    let key = req.query['input_text'];
    if (admin_keys.includes(key)){
        let information='Βλάβες με χρονολογική σειρά'
    model.getAll((err, rows) => {   
        if (err){
          console.log(err.message);
        } 
        //console.log('Recents', rows)
        res.render('admin_history', {layout : 'layout', search_results:rows,information:information});
      });
    }
    else{
            let error={'e_type':'undefined','message':'Το κλειδί σας δεν είναι σωστό'};
            res.render('admin_login', {layout : 'layout',error:error});
    }
    
      
};

let give_admin_page = function(req,res){
    let failure_id=req.query['failure_id'];
    model.get_failure_info(failure_id, (err, rows) => {   
        if (err){
          console.log(err.message);
        }
        let info_to_pass={};
        Object.assign(info_to_pass,rows[0]);
     
        info_to_pass['coords_to_show_x']=(info_to_pass['coordinates_x']*x_ratio+x0);
        info_to_pass['coords_to_show_y']=(info_to_pass['coordinates_y']*y_ratio+y0);
        
        //console.log(rows)
        res.render('admin_page', {layout : 'layout', failure_info:info_to_pass, buildings : buildings, categories : categories, states:states});
      });
      
};


let give_failure_page = function(req,res){
    let failure_id=req.query['failure_id'];
    model.get_failure_info(failure_id, (err, rows) => {   
        if (err){
          console.log(err.message);
        } 
        //console.log(rows)
        let info_to_pass={};
        Object.assign(info_to_pass,rows[0]);
       
        info_to_pass['coords_to_show_x']=(info_to_pass['coordinates_x']*x_ratio+x0);
        info_to_pass['coords_to_show_y']=(info_to_pass['coordinates_y']*y_ratio+y0);
        
        //console.log(info_to_pass);
        res.render('failure', {layout : 'layout',failure_info:info_to_pass});
      });
    // Παίρνω όλα τα πεδία και κάνω δυναμικό plot με handlebars, δες στο αρχείο του failure
    //console.log(failure_id);
    //check if serial number (the id) exists in failure table and insert the coresponding failure info into the failure_info bellow
    // fed ton an #each helper), we can use #with if we end up using just 1 item but each works pretty much the same and leaves the possibility for more than one )

};

let give_report_page = function(req,res){

    let error={'e_type':'','message':''};
    res.render('report', {layout : 'layout', buildings : buildings, categories : categories,error:error });


};

let is_it_valid_report= function(report_info){
    if (report_info.hasOwnProperty('fileValidationError')) {
        console.log("image didn't pass validation");
       return false;
    }
    return true; //maybe add validity check later

};

let current_datetime = function(req,res){
  let today = new Date();
  let year = String(today.getFullYear());
  let month = String(today.getMonth() + 1);
  if (month.length == 1){
    month = '0' + month;
  }
  let day = String(today.getDate());
  if (day.length == 1){
    day = '0' + day;
  }
  let date = year + '-' + month + '-' + day;
  let time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
  
  let now = date + ' ' + time;
  return now;
}

let submit_report = function(req,res){
    if (is_it_valid_report(req)){
        let info = req.body
        //console.log(req);
        let image_path = String(req.files[0].destination) + '/' + String(req.files[0].filename);
        image_path=image_path.replace('public/','');
        //console.log(req)    
        model.find_biggest_location_id((err, rows_1) => {   
            if (err){
                console.log('find_biggest_location_id');
                console.log(err.message);
            } 
        let location_info={'id':rows_1[0]['id']+1, 'building':info['building'], 'coordinates_x':info['West'],'coordinates_y': info['North']};
        model.push_location_in_db(location_info,(err, rows_2) => {   
            if (err){
                console.log('push_location_in_db');
                console.log(err.message);
            } 
        model.find_biggest_failure_id((err, rows_3) => {   
            if (err){
                console.log('find_biggest_failure_id');
                console.log(err.message);
            } 
            let now = current_datetime();
            console.log(now);
            let failure_data={'id':rows_3[0]['id']+1, 'title':info['title'],'description':info['description'],'creation_date':now,'closure_date':null,'state': 'Υπό επεξεργασία','image_path':image_path,'contact_phone':info['phone'],'contact_email':info['email'],'locale':rows_1[0]['id']+1,'category':info['category']};//change type atribute frome 1 to info['category]
            model.push_failure_in_db(failure_data,(err, rows_4) => {   
                if (err){
                    console.log(err.message);
                } 
                let id_dict_to_pass={'failure_id_passed':failure_data['id']}
                //console.log(id_dict_to_pass['i'])
                //console.log(info);
                let mailOptions = {
                    from: 'unireportuniversityofpatras@gmail.com',
                    to: String(info['email']),
                    subject: 'Αναφορά βλάβης',
                    text: "Αυτή η απάντηση είναι αυτοματοποιημένη. Η αναφορά σας στην πλατφόρμα 'Uni Report' του Πανεπιστημίου Πατρών καταχωρήθηκε με σειριακό κωδικό: '"+String(failure_data['id'])+"' . Μπορείτε να παρακολουθήσετε την εξέλιξη της βλάβης στην σελίδα της υπηρεσίας εισάγοντας στην γραμμή αναζήτησης τον κωδικό της βλάβης. Τίτλος βλάβης: "+String(failure_data['title']),
                  };
                  
                  if(mailOptions.to){
                    transporter.sendMail(mailOptions, function(error, info){
                        if (error) {
                          console.log(error);
                        } else {
                          console.log('Email sent: ' + info.response);
                        }
                      }); 
                  }

                res.render('successful_report', {layout : 'layout', id_dict_to_pass:id_dict_to_pass});
                });
            });
        });
    }); 
        //console.log(info);
        //console.log(image_path);
        //// add query to push new report_type entry in db using report info
        //// also add code to save image in disc and set a path that will be inputed in the db
    }
    else{
        let error={'e_type':'undefined','message':'Η υποβολή ήταν ανεπιτυχής'};
        res.render('report', {layout : 'layout', buildings : buildings, categories : categories, error:error  });

    }

};

let is_empty = function(v){
  if (v.length && v == ''){
    return [1];
  }

  for (let i =0; i < v.length; i++){
    if (v[i] != ''){
      if(Array.isArray(v)){
        return [0,v[i]]
      }
      return [0];
    }
  }
  return [1];
}

let filter = function(body){
  let ticket_info = {};
  let locale_info = {};
  let l = ['building', 'coordinates_x', 'coordinates_y'];
  for (const [key, value] of Object.entries(body)) {
    //console.log(key, value);
    let e = is_empty(value)
    console.log(e)
    if(e[0]){
      delete body[key];
    }
    else{
      if(l.includes(key)){
        if(e.length == 1){
          locale_info[key] = value;
        }
        else{
          locale_info[key] = e[1];
        }
      }
      else{
        if(e.length == 1){
          ticket_info[key] = value;
        }
        else{
          ticket_info[key] = e[1];
        }
      }
    }
  }
  return {
    'ticket_info': ticket_info,
    'locale_info': locale_info
  };
}



let admin_update = function(req,res){
  let failure_id=req.query['failure_id'];
  let locale_id=req.query['locale_id'];
  let body = req.body;
  console.log(body)
  let filtered_body = filter(body);
  
  let ticket_info = filtered_body.ticket_info;
  let locale_info = filtered_body.locale_info;
  
  if(ticket_info['state']){
    if(ticket_info['state'] == 'Κλειστή'){
      ticket_info['closure_date'] = current_datetime();
    }
  }
  if(req.files.length > 0){
    let image_path = String(String(req.files[0].destination) + '/' + String(req.files[0].filename));
    image_path=image_path.replace('public/','');
    ticket_info['image_path'] = image_path;
  }
  console.log(ticket_info,locale_info)
  //console.log(filtered_body)
  model.update_report(failure_id, locale_id, ticket_info, locale_info, (err) => {   
    if (err){
      console.log(err.message);
    } 
    res.redirect(String('/admin_page?failure_id=' + failure_id));
  });
};


let contractor_update = function(req,res){
  let failure_id=req.query['failure_id'];
  let locale_id=req.query['locale_id'];
  let key=req.query['key'];
  let body = req.body;
  console.log(body)
  let filtered_body = filter(body);
  
  let ticket_info = filtered_body.ticket_info;
  let locale_info = filtered_body.locale_info;
  
  if(ticket_info['state']){
    if(ticket_info['state'] == 'Κλειστή'){
      ticket_info['closure_date'] = current_datetime();
    }
  }
  //console.log(filtered_body)
  model.update_report(failure_id, locale_id, ticket_info, locale_info, (err) => {   
    if (err){
      console.log(err.message);
    } 
    res.redirect(String('/contractor_page?input_text=' + key));
  });



};

let delete_report = function(req,res){
  let information='Βλάβες με χρονολογική σειρά'
  let failure_id=req.query['failure_id'];
      model.delete_report(failure_id, (err, rows) => {   
          if (err){
              console.log(err.message);
          }
          res.render('admin_history', {layout : 'layout', search_results:rows,information:information});
      });
};

////////////////////////////////////////////////////////////////////////////////////////////////////////////// express routes
app.use(router);
router.route('/').get(give_home_page);
router.route('/open_failures').get(return_open_failures);
router.route('/report').get(give_report_page);
router.route('/history').get(give_history_page);
router.route('/search').get(give_result_page);
router.route('/failure').get(give_failure_page);
router.route('/report_complete').post(upload.any(), submit_report);
router.route('/contractor_login').get(give_contractor_login_page);
router.route('/contractor_page').get(give_contractor_page);
router.route('/contractor_update').post(upload.any(),contractor_update);
router.route('/admin_login').get(give_admin_login_page);
router.route('/admin_history').get(give_admin_history);
router.route('/admin_page').get(give_admin_page);
router.route('/admin_update').post(upload.any(),admin_update);
router.route('/delete_report').post(delete_report);
////////////////////////////////////////////////////////////////////////////////////////////////////////// initializing server
app.listen(port, () => console.log(`App listening to port ${port}`));