import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datas as datas
import create_csvs_intergrated as csv_maker
##############################################
import matplotlib
import matplotlib.pyplot as plt


class Statplot:
    def __init__(self, width, height, xpos, ypos, frames):
        self.w = width
        self.h = height
        self.posX = xpos
        self.posY = ypos
        self.photo = 'empty'

    def xyplot(self, title, xlabel, ylabel, datax, datay):

        fig = plt.figure()
        plt.plot(datax, datay)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        # plt.show()
        plt.savefig('temp.png')
        self.photo = tk.PhotoImage(file="temp.png")
        myDisplay.clear_display()
        label = tk.Label(frames[2])
        label.configure(image=self.photo)
        label.grid(row=0, column=0)

    def piChart(self, title, datax, datay):

        fig = plt.figure()
        plt.pie(datay, labels=datax, autopct='%1.0f%%',
                pctdistance=1.1, labeldistance=1.2)
        plt.savefig('temp.png')
        self.photo = tk.PhotoImage(file="temp.png")
        myDisplay.clear_display()
        label = tk.Label(frames[2])
        label.configure(image=self.photo)
        label.grid(row=0, column=0)

    def barChart(self, title, xlabel, ylabel, datax, datay):

        fig = plt.figure()
        # creating the bar plot
        plt.bar(datax, datay, color='maroon',
                width=0.4)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)

        plt.savefig('temp.png')
        self.photo = tk.PhotoImage(file="temp.png")
        myDisplay.clear_display()
        label = tk.Label(frames[2])
        label.configure(image=self.photo)
        label.grid(row=0, column=0)

    def move_figure(self, f, x, y):
        #"""Move figure's upper left corner to pixel (x, y)"""
        backend = matplotlib.get_backend()
        if backend == 'TkAgg':
            f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
        elif backend == 'WXAgg':
            f.canvas.manager.window.SetPosition((x, y))
        else:
            # This works for QT and GTK
            # You can also use window.setGeometry
            f.canvas.manager.window.move(x, y)
###################################################################################


entities_properties = {

    'Location': {"id": ['integer', True], "building": ['string', False], "coordinates_x": ['integer', False], "coordinates_y": ['integer', False]},

    'Ticket': {"id": ['integer', True], "title": ['string', False], "description": ['text', False], "creation_date": ['date', False],
               "closure_date": ['date', False], "state": ['string', False], "image_path": ['string', False], "ip": ['string', False], "contact_phone": ['string', False], "contact_email": ['string', False],
               "locale": ['integer', False, 'Location', 'id'], "category": ['string', False]},

    'Contract': {"id": ['integer', True], "key": ['string', False, True], "details": ['text', False], "date": ['date', False],
                 "cost": ['float', False], "damage": ['integer', False, 'Ticket', 'id'], "technician_firstname": ['string', False], "technician_lastname": ['string', False]}
}

# make a programm to scan the database and fill the dictionary based on the entities on the database


try:
    with open("data/Our_App.db") as f:
        print('database exists')

except IOError:
    print('database doesnt exist')
    print('creating with test data ...')
    # inp = input(" do you want to fabricate test data?\n y/n:")
    # if inp == 'y':
    csv_maker.create_all()
    # else:
    #     for i in list(entities_properties.keys()):
    #         f = open('data/{}.csv'.format(i), 'w')
    #         f.close()

d = datas.DataModel('data/Our_App', entities_properties)


class Result():
    def __init__(self, frame, entity_name, string, grid_row, conf):
        self.frame = frame
        self.conf = conf
        self.info = string
        self.grid_row = grid_row
        self.entity_name = entity_name
        self.view_button = tk.Button(frame, text=self.info[0], command=self.view1, width=conf['result_button_width'], bd=conf['result_button_border_width'],
                                     height=conf['result_button_height'], bg=conf['result_button_background_color'], font=conf['result_buttons_font'])
        self.view_button.grid(row=grid_row, column=0)
        self.attributes = list(conf['entities_properties'][entity_name].keys())
        self.edit_button = tk.Button(frame, text='  edit  ', command=self.edit1, width=conf['result2_button_width'], bd=conf['result2_button_border_width'],
                                     height=conf['result2_button_height'], bg=conf['result2_button_background_color'], font=conf['result2_buttons_font'])
        self.edit_button.grid(row=grid_row, column=1)

        self.delete_button = tk.Button(frame, text='delete', bitmap="error", command=self.delete1, width=conf['result3_button_width'], bd=conf[
                                       'result3_button_border_width'], height=conf['result3_button_height'], bg=conf['result3_button_background_color'], font=conf['result3_buttons_font'])
        self.delete_button.grid(row=grid_row, column=2)

    def view1(self):
        s = '  Entity type : {}\n\n'.format(self.entity_name)
        k = -1
        for i in self.info:
            if i == '':
                r = 'NULL'
            else:
                r = i
            k = k+1
            s = s+'  {} : {}\n'.format(self.attributes[k], r)
        myDisplay.print_to_display(s)

    def delete1(self, only_db=False):
        if only_db == False:
            self.view_button.grid_forget()
            self.edit_button.grid_forget()
            self.delete_button.grid_forget()
        deletion_dict = {}
        deletion_dict[self.attributes[0]] = '='+self.info[0]
        if d.deleteRow(self.entity_name, deletion_dict) == False:
            messagebox.showerror("Error", "Delete failed")

        else:
            plhr = d.search(glob_quer[0], glob_quer[1])
            if plhr != False:
                show_results(plhr, glob_quer[0],
                             self.conf, start=starts, end=ends)

    def edit1(self):
        ####### open new window ####################################
        conf = self.conf
        temp_window = tk.Tk()
        temp_window.title('Edit')
        temp_window.geometry("{}x{}".format(
            conf['search1_x'], conf['search1_y']))
        temp_window.configure(bg=conf['search1_bg_color'])
        new_entry_2(temp_window, self.entity_name, conf, instruction=False, buttons=[
        ], mode=True, it=self.info, key=self.attributes[0])

        # self.delete1(only_db=True)


class Display():
    def __init__(self, frame):
        self.frame = frame
        self.history = []
        self.position = -1

    def print_to_display(self, string):
        self.history.append(string)
        self.position = self.position+1
        self.clear_display()
        show = tk.Label(self.frame, text=string, font=('Courier', 14, 'bold'),
                        height=24, width=70, bg='#faf0dc', justify='left', anchor='w')
        show.grid(row=0, column=0)

    def clear_display(self):
        self.position = self.position+1
        self.history.append('')
        for widgets in self.frame.winfo_children():
            widgets.destroy()

    def go_back(self):
        pass


def set_main_frames(main_window, conf):
    options_frame = tk.Frame(
        main_window, bg=conf['options_color'], height=conf['options_height'], width=conf['options_width'])
    options_frame.grid(column=0, row=0, columnspan=3)
    options_frame.grid_propagate(0)

    results_frame = tk.Frame(main_window, bg=conf['results_color'], height=(
        conf['y_main_res']-conf['options_height']), width=conf['results_width'])
    results_frame.grid(column=0, row=1, rowspan=2)
    results_frame.grid_propagate(0)

    display_frame = tk.Frame(main_window, bg=conf['display_color'], height=(
        conf['y_main_res']-conf['options_height']-conf['display_controls_height']), width=conf['display_width'])
    display_frame.grid(column=1, row=1, rowspan=1)
    display_frame.grid_propagate(0)

    tools_frame = tk.Frame(main_window, bg=conf['tools_color'], height=(
        conf['y_main_res']-conf['options_height']), width=conf['tools_width'])
    tools_frame.grid(column=2, row=1, rowspan=2)
    tools_frame.grid_propagate(0)

    display_controls_frame = tk.Frame(main_window, bg=conf['display_controls_color'],
                                      height=conf['display_controls_height'], width=conf['display_controls_frame_width'])
    display_controls_frame.grid(column=1, row=2)
    display_controls_frame.grid_propagate(0)
    return [options_frame, results_frame, display_frame, tools_frame, display_controls_frame]


def new_entry_1(conf):
    ####### open new window ####################################
    temp_window = tk.Tk()
    temp_window.title('New Entry')
    temp_window.geometry("{}x{}".format(conf['search1_x'], conf['search1_y']))
    temp_window.configure(bg=conf['search1_bg_color'])
    ###### add instruction widget and buttons #############################
    instruction = tk.Label(temp_window, text='  Choose an entity to enter  ', bg=conf['instruction_search1_background_color'], width=conf[
                           'search1_instruction_width'], height=conf['search1_button_height'], font=conf['search1_instruction_font'])
    instruction.grid(row=0, column=0)
    # make dynamic somehow? be carefull with lambda
    buttons = []
    entities = list(conf['entities_properties'].keys())
    #buttons.append(tk.Button(temp_window,text=entities[0],command= lambda:search2(temp_window,entities[0],conf,instruction,buttons)))
    # buttons[-1].grid(column=0,row=1)
    #buttons.append(tk.Button(temp_window,text=entities[1],command= lambda:search2(temp_window,entities[1],conf,instruction,buttons)))
    # buttons[-1].grid(column=0,row=2)
    ################

    k = 0
    for i in entities:
        k = k+1
        buttons.append(create_button_for_new_entry_1(
            temp_window, i, conf, instruction, buttons, k))


def create_button_for_new_entry_1(temp_window, entity, conf, instruction, buttons, step):
    button = tk.Button(temp_window, text=entity, command=lambda: new_entry_2(temp_window, entity, conf, instruction=instruction, buttons=buttons, mode=False, it=[]),
                       width=conf['search1_button_width'], bd=conf['search1_button_border_width'], height=conf['search1_button_height'], bg=conf['search1_button_background_color'], font=conf['search1_buttons_font'])
    button.grid(column=0, row=step)
    return button


def new_entry_2(temp_window, entity_name, conf, instruction=False, buttons=[], mode=False, it=[], key=False):
    global kslabels, kclicks

    ##### clearing window #######
    if instruction != False:
        instruction.grid_forget()
    for i in buttons:
        i.grid_forget()
    buttons = []

    #############################
    diction = conf['entities_properties']

    sub_diction = diction[entity_name]

    attributes = list(sub_diction.keys())
    temp_window.geometry("{}x{}".format(
        conf['new_entry2_x'], len(attributes)*conf['search2_y_mult']+60))
    klabels = []
    kslabels = []
    kentries = []
    kclicks = []
    k = -1
    for i in attributes:
        if len(sub_diction[i]) > 3:
            answers = None

            if len(d.search(sub_diction[i][2], answers)) == 0 and entity_name != 'Category':
                temp_window.destroy()
                return
        if sub_diction[i][0] == 'binary':  # fix
            k = k+1
            kclicks.append('')
            kslabels.append('')
            klabels.append(tk.Label(temp_window, text=i, width=conf['search2_label_width'], height=conf[
                           'search2_label_height'], bg=conf['search2_label_background_color'], font=conf['search2_label_font']))
            klabels[-1].grid(column=0, row=k)
            kentries.append(['entrybox', tk.Entry(temp_window)])
            if mode == True:
                kentries[-1][1].insert(0, it[k])
            else:
                kentries[-1][1].insert(0, 'add local path')
            kentries[-1][1].grid(column=1, row=k)

            continue
        elif len(sub_diction[i]) == 4:
            k = k+1
            ent = sub_diction[i][2]
            atr = sub_diction[i][3]
            possibles = d.search(ent, None)
            ind = list(diction[ent].keys()).index(atr)
            col = []
            for j in possibles:
                col.append(j[ind])
            temp_var = tk.StringVar()
            if mode == True:
                temp_var.set(it[k])
                kslabels.append(tk.Label(temp_window, text=it[k], width=12,
                                         height=conf['search2_label_height'], bg='white', bd=2, font=conf['search2_label_font']))
            else:
                kslabels.append(tk.Label(temp_window, text='choose', width=12,
                                height=conf['search2_label_height'], bg='white', bd=2, font=conf['search2_label_font']))
            kslabels[-1].grid(row=k, column=1)
            kclicks.append(temp_var)
            kentries.append(make_menu(temp_window, kclicks, col))
            klabels.append(tk.Label(temp_window, text=i, width=conf['search2_label_width'], height=conf[
                           'search2_label_height'], bg=conf['search2_label_background_color'], font=conf['search2_label_font']))
            klabels[-1].grid(column=0, row=k)
            kentries[-1][1].grid(column=2, row=k)
            continue
        elif sub_diction[i][1] == True:
            if mode == True:
                k = k+1
                kclicks.append('')
                kslabels.append('')
                kentries.append('')
                klabels.append('')
                continue
            ent = entity_name
            possibles = d.search(ent, None)
            col = []
            for j in possibles:
                col.append(int(j[0]))
            k = k+1
            kclicks.append('')
            kslabels.append('')
            klabels.append(tk.Label(temp_window, text=i, width=conf['search2_label_width'], height=conf[
                           'search2_label_height'], bg=conf['search2_label_background_color'], font=conf['search2_label_font']))
            klabels[-1].grid(column=0, row=k)
            kentries.append(['entrybox', tk.Entry(temp_window)])
            if mode == True:
                kentries[-1][1].insert(0, it[k])
            else:
                if len(d.search(entity_name, None)) == 0:
                    asking = 1
                else:
                    asking = max(col)+1
                kentries[-1][1].insert(0, '{}'.format(asking))

            kentries[-1][1].grid(column=1, row=k)

            continue

        elif sub_diction[i][0] == 'date':
            k = k+1
            kclicks.append('')
            kslabels.append('')
            klabels.append(tk.Label(temp_window, text=i, width=conf['search2_label_width'], height=conf[
                           'search2_label_height'], bg=conf['search2_label_background_color'], font=conf['search2_label_font']))
            klabels[-1].grid(column=0, row=k)
            kentries.append(['entrybox', tk.Entry(temp_window)])
            if mode == True:
                kentries[-1][1].insert(0, it[k])
            else:
                kentries[-1][1].insert(0, 'yyyy-mm-dd')
            kentries[-1][1].grid(column=1, row=k)

            continue
        else:
            k = k+1
            kclicks.append('')
            kslabels.append('')
            klabels.append(tk.Label(temp_window, text=i, width=conf['search2_label_width'], height=conf[
                           'search2_label_height'], bg=conf['search2_label_background_color'], font=conf['search2_label_font']))
            klabels[-1].grid(column=0, row=k)
            kentries.append(['entrybox', tk.Entry(temp_window)])
            if mode == True:
                kentries[-1][1].insert(0, it[k])
            kentries[-1][1].grid(column=1, row=k)
            continue

    enter = tk.Button(temp_window, text='Enter', command=lambda: new_entry_3(
        temp_window, entity_name, conf, kentries, kclicks, attributes, mode=mode, it=it, key=key), bg='orange', font=conf['search2_label_font'])
    enter.grid(column=0, columnspan=2, row=k+1)


def make_menu(temp_window, kclicks, col):
    # an valeis lambda edw vgainei to kraken to idio gtms
    return ['menu', tk.OptionMenu(temp_window, kclicks[-1], *col, command=set_menus)]


def set_menus(what):
    # print('eee?',what)
    global kslabels, kclicks

    for i in range(0, len(kslabels)):
        if kslabels[i] == '':
            continue
        else:
            kslabels[i].configure(text=kclicks[i].get())


def new_entry_3(temp_window, entity_name, conf, kentries, kclicks, attributes, mode=False, it=[], key=[]):
    answers = {}
    k = -1
    for i in attributes:
        k = k+1
        if kentries[k] == '':
            continue
        if kentries[k][0] == 'entrybox':
            answers[i] = kentries[k][1].get()
        else:
            answers[i] = kclicks[k].get()
    flag = 0
    for i in list(answers.keys()):
        if answers[i] == '' or answers[i] == 'yyyy-mm-dd':
            flag = i
            break
    if flag == 0:

        if mode == False:
            for i in list(answers.keys()):
                answers[i] = '='+answers[i]
            #print('\n\n\n\n', answers)
            if d.insertRow(entity_name, answers) == False:
                messagebox.showerror("Error", "New entry failed")
            else:
                if len(glob_quer) == 2:
                    plhr = d.search(glob_quer[0], glob_quer[1])
                    show_results(plhr, glob_quer[0],
                                 conf, start=starts, end=ends)
                temp_window.destroy()

        else:
            key_dict = {}
            key_dict[key] = '='+it[0]
            for i in list(answers.keys()):
                answers[i] = '='+answers[i]

            #print('\n\n\n\n', answers)
            if d.updateRow(entity_name, key_dict, answers) == False:
                # print('HEYYYYYYYYYYYY')
                messagebox.showerror("Error", "Edit failed")
            else:
                temp_window.destroy()
                plhr = d.search(glob_quer[0], glob_quer[1])
                show_results(plhr, glob_quer[0], conf, start=starts, end=ends)

    else:
        messagebox.showerror(
            "Error", "Insert failed , {} attribute was empty".format(i))

    # print(entity_name,answers)


def search1(conf):
    ####### open new window ####################################
    temp_window = tk.Tk()
    temp_window.title(conf['search_title'])
    temp_window.geometry("{}x{}".format(conf['search1_x'], conf['search1_y']))
    temp_window.configure(bg=conf['search1_bg_color'])
    ###### add instruction widget and buttons #############################
    instruction = tk.Label(temp_window, text='  Choose an entity to search  ', bg=conf['instruction_search1_background_color'], width=conf[
                           'search1_instruction_width'], height=conf['search1_button_height'], font=conf['search1_instruction_font'])
    instruction.grid(row=0, column=0)
    # make dynamic somehow? be carefull with lambda
    buttons = []
    entities = list(conf['entities_properties'].keys())
    #buttons.append(tk.Button(temp_window,text=entities[0],command= lambda:search2(temp_window,entities[0],conf,instruction,buttons)))
    # buttons[-1].grid(column=0,row=1)
    #buttons.append(tk.Button(temp_window,text=entities[1],command= lambda:search2(temp_window,entities[1],conf,instruction,buttons)))
    # buttons[-1].grid(column=0,row=2)
    ################

    k = 0
    for i in entities:
        k = k+1
        buttons.append(create_button_for_search1(
            temp_window, i, conf, instruction, buttons, k))


def create_button_for_search1(temp_window, entity, conf, instruction, buttons, step):
    button = tk.Button(temp_window, text=entity, command=lambda: search2(temp_window, entity, conf, instruction, buttons),
                       width=conf['search1_button_width'], bd=conf['search1_button_border_width'], height=conf['search1_button_height'], bg=conf['search1_button_background_color'], font=conf['search1_buttons_font'])
    button.grid(column=0, row=step)
    return button
    ##########################################################################


def req(conf, frame):

    buttons = []
    entities = list(conf['entities_properties'].keys())

    k = 0
    for i in entities:
        k = k+1
        buttons.append(create_button_for_req(frame, i, conf, k))


def req2(entity, conf):
    global glob_quer
    answers = None
    glob_quer = [entity, answers]
    strings = d.search(entity, answers)
    show_results(strings, entity, conf)


def create_button_for_req(frame, entity, conf, step):
    button = tk.Button(frame, text=entity, command=lambda: req2(entity, conf), width=conf['search1_button_width'], bd=conf[
                       'search1_button_border_width'], height=conf['search1_button_height'], bg=conf['search1_button_background_color'], font=conf['search1_buttons_font'])
    button.grid(column=0, row=step)
    return button
    ##########################################################################


def search2(temp_window, entity_name, conf, instruction, buttons):

    ##### clearing window #######
    instruction.grid_forget()
    for i in buttons:
        i.grid_forget()
    buttons = []

    #############################
    diction = conf['entities_properties']

    sub_diction = diction[entity_name]

    attributes = list(sub_diction.keys())
    temp_window.geometry("{}x{}".format(
        conf['search2_x'], len(attributes)*conf['search2_y_mult']+30))
    labels = []
    k = 0
    for i in attributes:
        if sub_diction[i][0] != 'binary':
            k = k+1
            labels.append(tk.Label(temp_window, text=i, width=conf['search2_label_width'], height=conf[
                          'search2_label_height'], bg=conf['search2_label_background_color'], font=conf['search2_label_font']))
            labels[-1].grid(column=0, row=k, sticky='W')

    entries = []
    spacers1 = []
    spacers2 = []
    k = 0
    ats = []
    for i in attributes:
        if sub_diction[i][0] != 'binary':
            ats.append(i)
            k = k+1
            if sub_diction[i][0] == 'text':
                entries.append([tk.Entry(temp_window)])
                entries[-1][0].grid(column=2, row=k)
                spacers1.append(tk.Label(temp_window, text='is', width=conf['search2_spacer_width'], height=conf[
                                'search2_spacer_height'], bg=conf['search2_spacer_background_color'], font=conf['search2_spacer_font']))
                spacers1[-1].grid(row=k, column=1)
            elif sub_diction[i][0] == 'date':
                entries.append([tk.Entry(temp_window), tk.Entry(temp_window)])
                entries[-1][0].grid(column=2, row=k)
                entries[-1][0].insert(string="yyyy-mm-dd", index=1)
                entries[-1][1].grid(column=4, row=k)
                entries[-1][1].insert(string="yyyy-mm-dd", index=1)
                spacers1.append(tk.Label(temp_window, text=' above ', width=conf['search2_spacer_width'], height=conf[
                                'search2_spacer_height'], bg=conf['search2_spacer_background_color'], font=conf['search2_spacer_font']))
                spacers1[-1].grid(row=k, column=1)
                spacers2.append(tk.Label(temp_window, text='below', width=conf['search2_spacer_width'], height=conf[
                                'search2_spacer_height'], bg=conf['search2_spacer_background_color'], font=conf['search2_spacer_font']))
                spacers2[-1].grid(row=k, column=3)
            else:
                entries.append([tk.Entry(temp_window), tk.Entry(temp_window)])
                entries[-1][0].grid(column=2, row=k)
                entries[-1][1].grid(column=4, row=k)
                spacers1.append(tk.Label(temp_window, text=' above ', width=conf['search2_spacer_width'], height=conf[
                                'search2_spacer_height'], bg=conf['search2_spacer_background_color'], font=conf['search2_spacer_font']))
                spacers1[-1].grid(row=k, column=1)
                spacers2.append(tk.Label(temp_window, text='below', width=conf['search2_spacer_width'], height=conf[
                                'search2_spacer_height'], bg=conf['search2_spacer_background_color'], font=conf['search2_spacer_font']))
                spacers2[-1].grid(row=k, column=3)

    enter = tk.Button(temp_window, text='Enter', command=lambda: search3(
        temp_window, entity_name, conf, entries, ats), bg='orange', font=conf['search2_label_font'])
    enter.grid(column=0, columnspan=2, row=k+1)


def search3(temp_window, entity_name, conf, entries, ats):
    global glob_quer
    answers = {}
    for i in range(0, len(entries)):
        if len(entries[i]) == 1:
            if entries[i][0].get() != '':
                answers[ats[i]] = '='+entries[i][0].get()
                continue
            else:
                continue

        else:
            if entries[i][0].get() == "yyyy-mm-dd" and entries[i][1].get() == "yyyy-mm-dd":
                continue
            if entries[i][0].get() == "yyyy-mm-dd":
                answers[ats[i]] = '='+entries[i][1].get()
                continue
            if entries[i][1].get() == "yyyy-mm-dd":
                answers[ats[i]] = '='+entries[i][0].get()
                continue
            if '_' in entries[i][0].get() and '_' in entries[i][1].get():
                answers[ats[i]] = '<{}&>{}'.format(
                    entries[i][1].get(), entries[i][0].get())
                continue
            if entries[i][0].get() == '' and entries[i][1].get() == '':
                continue
            if entries[i][0].get() == '':
                answers[ats[i]] = '<'+entries[i][1].get()
                continue
            if entries[i][1].get() == '':
                answers[ats[i]] = '>'+entries[i][0].get()
                continue
            answers[ats[i]] = '<{}&>{}'.format(
                entries[i][1].get(), entries[i][0].get())

    if len(list(answers.keys())) == 0:
        answers = None
    strings = d.search(entity_name, answers)

    if strings == False:
        messagebox.showerror("Error", "Search failed")
    elif len(strings) == 0:
        messagebox.showerror("Error", "Nothing found")

    else:
        glob_quer = [entity_name, answers]
        show_results(strings, entity_name, conf)
        # print(answers)
        # print(entity_name) ############use stauros search function here
        temp_window.destroy()


def show_tree(strings, entity_name, conf):
    ####### open new window ####################################
    columns = list(conf['entities_properties'][entity_name].keys())
    temp_window = tk.Tk()
    temp_window.title(conf['search_title'])
    temp_window.configure(bg=conf['search1_bg_color'])

    sb = tk.Scrollbar(temp_window, orient='vertical')
    sb.pack(side='right', fill='y')
    # myDisplay.clear_display()

    tree = ttk.Treeview(temp_window)
    tree['columns'] = columns
    tree.column('#0', width=0, stretch=False)
    tree.heading('#0', text='', anchor='center')
    total_width = 0
    for i in columns:
        width = 4*int(conf["display_width"]/(10+len(strings[0])))
        total_width += width
        tree.column(
            i, width=width, anchor='center')
        tree.heading(i, text=i, anchor='center')
    temp_window.geometry("{}x{}".format(total_width + 18, 300))
    k = -1
    for i in strings:  # this is slow
        # print(k)
        k = k+1
        tree.insert(parent='', index=k, iid=k, text='', values=i)
    tree.config(yscrollcommand=sb.set)
    sb.config(command=tree.yview)
    tree.pack(side='left', fill='y')


def clear_results():
    for widgets in frames[1].winfo_children():
        widgets.destroy()


def show_results(strings, entity_name, conf, start=0, end=20):
    global strings_glob, entity_glob, starts, ends
    starts = start
    ends = end
    strings_glob = strings
    entity_glob = entity_name

    # print(strings)
    clear_results()
    # print(strings)

    results = []
    k = 0
    information = tk.Label(frames[1], text='Entity type:\n {}\nby id'.format(
        entity_name), font=('Courier', 10, 'bold'), height=3, width=17, bg='yellow')
    information.grid(row=0, column=0, columnspan=1)
    for i in range(start, end):
        if i >= len(strings):
            break
        k = k+1
        results.append(Result(frames[1], entity_name, strings[i], k, conf))
    if True:
        show_all_button = tk.Button(frames[1], text='View\nAll', bg='yellow', font=(
            'Courier', 8, 'bold'), height=3, width=6, command=lambda: show_tree(strings, entity_name, conf))
        show_all_button.grid(row=0, column=2, sticky='W')
        clear_button = tk.Button(frames[1], text='Clear\nResults', bg='yellow', font=(
            'Courier', 8, 'bold'), height=3, width=8, command=clear_results)
        clear_button.grid(columnspan=1, row=0, column=1, sticky='W')
        if end < (len(strings)):
            next_button = tk.Button(frames[1], text=' Next', bg='yellow', font=('Courier', 12, 'bold'), height=3,
                                    width=11, command=lambda: show_results(strings_glob, entity_glob, conf, start=starts+20, end=ends+20))
            next_button.grid(columnspan=2, row=22, column=1, sticky='W')
        else:
            next_button = tk.Button(frames[1], text=' Next', bg='yellow', font=(
                'Courier', 12, 'bold'), height=3, width=11, command=lambda: messagebox.showerror("Error", "You have reached the end of time"))
            next_button.grid(columnspan=2, row=22, column=1, sticky='W')
        if start >= 20:
            past_button = tk.Button(frames[1], text=' Previous ', bg='yellow', font=(
                'Courier', 12, 'bold'), height=3, width=13, command=lambda: show_results(strings_glob, entity_glob, conf, start=starts-20, end=ends-20))
            past_button.grid(columnspan=1, row=22, column=0, sticky='W')
        else:
            past_button = tk.Button(frames[1], text=' Previous ', bg='yellow', font=(
                'Courier', 12, 'bold'), height=3, width=13, command=lambda: messagebox.showerror("Error", "You have reached the beggining of time"))
            past_button.grid(columnspan=1, row=22, column=0, sticky='W')
    return


def stats_age(temp_window):
    temp_window.destroy()
    to_plot = d.executeSQL('', txtFile='special queries/profits_age.txt')
    print(to_plot)
    datax = []
    datay = []
    for i in to_plot:
        datax.append(float(i[0]))
        datay.append(float(i[1]))
    my_stat.xyplot('Profits/Age', 'Ages', 'Profits', datax, datay)


def stats_genre(temp_window):
    temp_window.destroy()
    to_plot = d.executeSQL('', txtFile='special queries/profits_genre.txt')
    print(to_plot)
    datax = []
    datay = []
    for i in to_plot:
        datax.append(str(i[0]))
        datay.append(float(i[1]))
    my_stat.piChart('Profits/Genre', datax, datay)


def stats_city(temp_window):
    temp_window.destroy()
    to_plot = d.executeSQL('', txtFile='special queries/profits_city.txt')
    print(to_plot)
    datax = []
    datay = []
    for i in to_plot:
        datax.append(str(i[0]))
        datay.append(float(i[1]))
    my_stat.piChart('Profits/City', datax, datay)


def stats_window(conf):
    buttons = []
    ####### open new window ####################################
    temp_window = tk.Tk()
    temp_window.title('Statistics')
    temp_window.geometry("{}x{}".format(280, 200))
    temp_window.configure(bg=conf['search1_bg_color'])
    ###### add instruction widget and buttons #############################
    instruction = tk.Label(temp_window, text='  \nChoose a statistic \nto display  ', bg=conf['instruction_search1_background_color'], width=conf[
                           'search1_instruction_width'], height=3, font=conf['search1_instruction_font'])
    instruction.grid(row=0, column=0)
    temp = tk.Button(temp_window, text='Profits / Age', command=lambda: stats_age(temp_window), width=18,
                     bd=conf['options_button_border_width'], height=conf['options_button_height'], bg=conf['options_button_background_color'], font=conf['options_buttons_font'])
    temp.grid(row=1, column=0)
    buttons.append(temp)

    temp = tk.Button(temp_window, text='Profits / Genre', command=lambda: stats_genre(temp_window), width=18,
                     bd=conf['options_button_border_width'], height=conf['options_button_height'], bg=conf['options_button_background_color'], font=conf['options_buttons_font'])
    temp.grid(row=2, column=0)
    buttons.append(temp)

    temp = tk.Button(temp_window, text='Profits / City', command=lambda: stats_city(temp_window), width=18,
                     bd=conf['options_button_border_width'], height=conf['options_button_height'], bg=conf['options_button_background_color'], font=conf['options_buttons_font'])
    temp.grid(row=3, column=0)
    buttons.append(temp)


def set_options(frame, conf):
    buttons = []
    lbl = tk.Label(frame, height=1, width=26, text='_______| Results |________',
                   bg='#c6ad8f', font=conf['options_buttons_font'])
    lbl.grid(column=0, row=0)
    temp = tk.Button(frame, text='Search', command=lambda: search1(conf), width=conf['options_button_width'], bd=conf['options_button_border_width'],
                     height=conf['options_button_height'], bg=conf['options_button_background_color'], font=conf['options_buttons_font'])
    temp.grid(row=0, column=1)
    buttons.append(temp)

    temp = tk.Button(frame, text='New entry', command=lambda: new_entry_1(
        conf), width=conf['options_button_width'], bd=conf['options_button_border_width'], height=conf['options_button_height'], bg=conf['options_button_background_color'], font=conf['options_buttons_font'])
    temp.grid(row=0, column=2)
    buttons.append(temp)

    # temp = tk.Button(frame, text='Statistics', command=lambda: stats_window(
    #     conf), width=conf['options_button_width'], bd=conf['options_button_border_width'], height=conf['options_button_height'], bg=conf['options_button_background_color'], font=conf['options_buttons_font'])
    # temp.grid(row=0, column=3)
    # buttons.append(temp)
    # return buttons


configuration = {
    "x_main_res": 1124,
    "y_main_res": 800,
    "main_title": 'OurApp',
    "options_height": 27,  # 26 or smaller if we don't want the options_bg_color showing
    "results_width": 266,
    "display_controls_height": 32,
    "display_width": 656,
    "options_width": 1124,
    "tools_width": 200,
    "display_controls_frame_width": 660,
    'options_color': '#c6ad8f',
    'results_color': '#c6ad8f',
    'display_color': '#faf0dc',
    'tools_color': '#c6ad8f',
    'display_controls_color': '#c6ad8f',
    'options_button_border_width': 2,
    'options_button_background_color': '#c6ad8f',
    'options_button_width': 10,
    'options_button_height': 1,
    'options_buttons_font': ('Courier', 12, 'bold'),
    'search_title': 'Enter search settings',
    'search1_x': 280,
    'search1_y': 450,
    'search2_x': 750,
    'search2_y_mult': 31,
    'search1_bg_color': '#c6ad8f',
    'entities_properties': entities_properties,
    'search1_button_border_width': 2,
    'search1_button_background_color': '#c6ad8f',
    'search1_button_width': 20,
    'search1_button_height': 1,
    'search1_buttons_font': ('Courier', 12, 'bold'),
    'search2_label_width': 25,
    'search2_label_height': 1,
    'search2_label_background_color': '#c6ad8f',
    'search2_label_font': ('Courier', 15, 'bold'),
    'instruction_search1_background_color': '#c6ad8f',
    'search1_instruction_font': ('Courier', 12, 'bold'),
    'search1_instruction_width': 28,
    'search2_spacer_width': 6,
    'search2_spacer_height': 1,
    'search2_spacer_background_color': '#c6ad8f',
    'search2_spacer_font': ('Courier', 15, 'bold'),
    'result_button_border_width': 2,
    'result_button_background_color': 'light blue',
    'result_button_width': 13,
    'result_button_height': 1,
    'result_buttons_font': ('Courier', 12, 'bold'),
    'result2_button_border_width': 2,
    'result2_button_background_color': 'green',
    'result2_button_width': 5,
    'result2_button_height': 1,
    'result2_buttons_font': ('Courier', 12, 'bold'),
    'result3_button_border_width': 2,
    'result3_button_background_color': 'red',
    'result3_button_width': 45,
    'result3_button_height': 26,
    'result3_buttons_font': ('Courier', 12, 'bold'),
    'new_entry2_x': 500



}

##############################################
main_w = tk.Tk()
main_w.geometry("{}x{}".format(
    configuration['x_main_res'], configuration['y_main_res']))
main_w.title(configuration['main_title'])
frames = set_main_frames(main_w, configuration)
configuration['frames'] = frames
myDisplay = Display(frames[2])

width, height, xpos, ypos = [512, 512, 256, 256]
my_stat = Statplot(width, height, xpos, ypos, frames)

# options_frame 0 ,results_frame 1 ,display_frame 2 ,tools_frame 3 ,display_controls_frame 4
# frames[0].configure(bg='black')
req(configuration, frames[3])
options_buttons = set_options(frames[0], configuration)

clear_display_button = tk.Button(frames[4], text='Clear Display', bg='#c6ad8f', font=(
    'Courier', 12, 'bold'), height=1, width=14, command=myDisplay.clear_display)
clear_display_button.grid(row=0, column=0)


# res=Result(frames[1],'hi',1,configuration)
#MyLabel = tk.Label(frames[1],text="Labe",height='5',width='20',bg='orange')
# MyLabel.grid(row=0,column=0)
#MyLabel2 = tk.Label(frames[1],text="LabeLSSS",height='5',width='20',bg='orange')
# MyLabel2.grid(row=1,column=0)

###################
main_w.mainloop()
d.close()
###################
