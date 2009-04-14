import wx
import wx.aui
import wx.lib
import numpy
import string ,re
#import models
_BOX_WIDTH = 80
import basepage

class PageInfo(object):
    """
        this class contains the minimum numbers of data members
        a fitpage or model page need to be initialized.
    """
    data = None
    model= None
    manager= None
    event_owner= None
    model_list_box = None
    name=None
     ## Internal name for the AUI manager
    window_name = "Page"
    ## Title to appear on top of the window
    window_caption = "Page"
    
    def __init__(self, model=None,data=None, manager=None,
                  event_owner=None,model_list_box=None , name=None):
        """
            Initialize data members
        """
        self.data = data
        self.model= model
        self.manager= manager
        self.event_owner= event_owner
        self.model_list_box = model_list_box
        self.name=None
        self.window_name = "Page"
        self.window_caption = "Page"
    
class FitPanel(wx.aui.AuiNotebook):    

    """
        FitPanel class contains fields allowing to fit  models and  data
        @note: For Fit to be performed the user should check at least one parameter
        on fit Panel window.
       
    """
    ## Internal name for the AUI manager
    window_name = "Fit panel"
    ## Title to appear on top of the window
    window_caption = "Fit Panel "
    CENTER_PANE = True
    def __init__(self, parent, *args, **kwargs):
        wx.aui.AuiNotebook.__init__(self,parent,-1, style=wx.aui.AUI_NB_DEFAULT_STYLE  )
        
        
        self.manager=None
        self.parent=parent
        self.event_owner=None
        
        pageClosedEvent = wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.onClosePage)
        #Creating the default page --welcomed page
        self.about_page=None
        from welcome_panel import PanelAbout
        self.about_page = PanelAbout(self, -1)
        self.AddPage(self.about_page,"welcome!")
      
       
        #dictionary of miodel {model class name, model class}
        self.model_list_box={}
        ##dictionary of page info
        self.page_info_dict={}
        ## save the title of the last page tab added
        self.fit_page_name={}
        ## list of existing fit page
        self.list_fitpage_name=[]
    
        #model page info
        self.model_page_number=None
       
        self.model_page=None
        self.sim_page=None
        ## get the state of a page
        self.Bind(basepage.EVT_PAGE_INFO, self._onGetstate)
        # increment number for model name
        self.count=0
        #updating the panel
        self.Update()
        self.Center()
        
        
    def onClosePage(self, event):
        """
             close page and remove all references to the closed page
        """
        selected_page = self.GetPage(self.GetSelection())
        ## removing about page
        if selected_page==self.about_page:
            self.about_page=None
            return 
        ## removing sim_page
        if selected_page == self.sim_page:
            self.manager.sim_page=None 
            return
        
        ## closing other pages
        state = selected_page.createMemento()
        page_name = selected_page.window_name
        page_finder = self.manager.get_page_finder() 
        fitproblem = None
        ## removing model page
        if selected_page == self.model_page:
            fitproblem = selected_page.model.clone()
            self.model_page = None
            self.count =0
            ## page on menu
            self.manager._add_page_onmenu(page_name, fitproblem)
        else:
            if selected_page in page_finder:
       
                fitproblem= page_finder[selected_page].clone()
                ## page on menu
                self.manager._add_page_onmenu(page_name, fitproblem)
                del page_finder[selected_page]
            ##remove the check box link to the model name of this page (selected_page)
            try:
                self.sim_page.draw_page()
            except:
                ## that page is already deleted no need to remove check box on
                ##non existing page
                pass
                
        #Delete the name of the page into the list of open page
        if selected_page.window_name in self.list_fitpage_name:
            self.list_fitpage_name.remove(selected_page.window_name)
            
        
    def set_manager(self, manager):
        """
             set panel manager
             @param manager: instance of plugin fitting
        """
        self.manager = manager

        
    def set_owner(self,owner):
        """ 
            set and owner for fitpanel
            @param owner: the class responsible of plotting
        """
        self.event_owner = owner
    
    def set_model_list(self,dict):
         """ 
             copy a dictionary of model into its own dictionary
             @param dict: dictionnary made of model name as key and model class
             as value
         """
         self.model_list_box = dict
        
  
    def get_current_page(self):
        """
            @return the current page selected
        """
        return self.GetPage(self.GetSelection() )
    
    def add_sim_page(self):
        """
            Add the simultaneous fit page
        """
        from simfitpage import SimultaneousFitPage
        page_finder= self.manager.get_page_finder()
        self.sim_page = SimultaneousFitPage(self,page_finder=page_finder, id=-1)
        
        self.AddPage(self.sim_page,caption="Simultaneous Fit",select=True)
        self.sim_page.set_manager(self.manager)
        return self.sim_page
        
    def add_fit_page( self,data, reset=False ):
        """ 
            Add a fitting page on the notebook contained by fitpanel
            @param data: data to fit
            @return panel : page just added for further used. is used by fitting module
        """     
        try:
            name = data.name 
        except:
            name = 'Fit'
        if not name in self.list_fitpage_name:
            myinfo = PageInfo( data=data, name=name )
            myinfo.model_list_box = self.model_list_box.get_list()
            myinfo.event_owner = self.event_owner 
            myinfo.manager = self.manager
            myinfo.window_name = name
            myinfo.window_caption = name
        
            #if not name in self.fit_page_name :
            from fitpage import FitPage
            panel = FitPage(parent= self, page_info=myinfo)
            
            self.AddPage(page=panel, caption=name, select=True)
            self.list_fitpage_name.append(name)
            if reset:
                if name in self.fit_page_name.keys():
                    memento= self.fit_page_name[name][0]
                    panel.reset_page(memento)
            else:
                self.fit_page_name[name]=[]
                self.fit_page_name[name].insert(0,panel.createMemento())
         
            return panel 
        else:
            return None 
        
   
    def add_model_page(self,model,page_title="Model", qmin=0, qmax=0.1,
                        npts=50, topmenu=False, reset=False):
        """
            Add a model page only one  to display any model selected from the menu or the page combo box.
            when this page is closed than the user will be able to open a new one
            
            @param model: the model for which paramters will be changed
            @param page_title: the name of the page
            @param page_info: contains info about the state of the page
            @param qmin: mimimum Q
            @param qmax: maximum Q
            @param npts: number of Q points
        """
        if topmenu==True:
            ##first time to open model page
            if self.count==0 :
                #if not page_title in self.list_fitpage_name :
                self._help_add_model_page(model=model, page_title=page_title,
                                qmin=qmin, qmax=qmax, npts=npts, reset=reset)
                self.count +=1
            else:
                self.model_page.select_model(model, page_title)
                self.fit_page_name[page_title].insert(0,self.model_page.createMemento())
      
           
    def  _onGetstate(self, event):
        """
            copy the state of a page
        """
        page= event.page
        if page.window_name in self.fit_page_name:
            self.fit_page_name[page.window_name].insert(0,page.createMemento()) 
            
                
    def _help_add_model_page(self,model,page_title="Model", qmin=0, 
                             qmax=0.1, npts=50,reset= False):
        """
            #TODO: fill in description
            
            @param qmin: mimimum Q
            @param qmax: maximum Q
            @param npts: number of Q points
        """
        ## creating object that contaning info about model 
        myinfo = PageInfo(model= model ,name= page_title)
        myinfo.model_list_box = self.model_list_box.get_list()
        myinfo.event_owner = self.event_owner 
        myinfo.manager = self.manager
        myinfo.window_name = page_title
        myinfo.window_caption = page_title
      
        from modelpage import ModelPage
        panel = ModelPage(self,myinfo)
        
        self.AddPage(page=panel,caption=page_title,select=True)

        self.model_page_number=self.GetSelection()
        self.model_page=self.GetPage(self.GetSelection())
        # Set the range used to plot models
        self.model_page.set_range(qmin, qmax, npts)
        ##  resetting page
        if reset:
            if page_title in self.fit_page_name.keys():
                
                memento= self.fit_page_name[page_title][0]
                panel.reset_page(memento)
        else:
            self.fit_page_name[page_title]=[]
            self.fit_page_name[page_title].insert(0,panel.createMemento())
         
        # We just created a model page, we are ready to plot the model
        #self.manager.draw_model(model, model.name)
        #FOR PLUGIN  for some reason model.name is = BASEcomponent
        self.manager.draw_model(model)
  
  