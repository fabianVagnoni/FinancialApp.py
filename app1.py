# App's main file
# WARNING: After hitting the 'Submit' button the application will take approx. 20 seconds to do the plot
# Please, be patient


# Import necessary libraries
import kivy
from kivy.app import App
from kivy.properties import ObjectProperty,StringProperty
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.popup import Popup
import re
import plotter
from kivy.uix.image import Image
import modelling
import returnCalc


# Define the different classes that will be used for the pop-up windows to manage errors
# These classes are empty because all logic and structure will be managed on the .kv file
class P(Screen):
    pass


class P2(Screen):
    pass


class P3(Screen):
    pass


class PReturn(Screen):
    secReturn = StringProperty('')
    sec = StringProperty('')

    def __init__(self, secReturn='', sec='' , **kwargs):
        super(PReturn, self).__init__(**kwargs)
        self.secReturn = secReturn
        self.sec = sec
        print(self.sec)


# Starting Menu
class StartMenu(Screen):
    pass


# Define the class for the initial screen
class FirstScreen(Screen):
    # Define the global variables of ticker and timeSpan
    # These are initially empty, but will be filled by the user's input
    ticker = ObjectProperty(None)
    timeSpan = ObjectProperty(None)

    # Define the submit method that will be ran once the user press the submit button
    def submit(self):
        # The variable x will serve as a checking tool to see if everything is good
        x=0

        # Print the user's input texts
        print(self.ticker.text, self.timeSpan.text)

        # Check that the ticker inputted by the user matches any of the needed patterns:
        # 'MMMM' , 'MMM' , 'MMM.M' , '^MMM' , '^MMMM'
        # If the inputted ticker does not match, erase the input of the user and sum one to x
        patternTicker = r'(\^[A-Z]{3}C?)|^[A-Z]{3}(\.[A-Z])?$|^[A-Z]{4}$'
        if not bool(re.match(patternTicker, self.ticker.text)):
            print("Invalid ticker")
            self.ticker.text = ''
            x+=1

        # Check that the timeSpan matches the required pattern:
        # yyyy-mm-dd,yyyy-mm-dd
        # Where mm is a number such that (1<=mm<=12) and dd is a number such that (1<=dd<=31)
        # If the inputted timeSpan does not match, erase the input and sum one to x
        patternTime = r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01]),\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$'
        if not bool(re.match(patternTime, self.timeSpan.text)):
            print("Invalid Time Span")
            self.timeSpan.text = ''
            x+=1

        # If x is different from zero, some input was not manageable
        # Hence, show the first pop-up window with title 'Format Error'
        # Return None
        if x != 0:
            show = P()
            popupWindow = Popup(title="Format Error", content=show, size_hint=(None, None), size=(700,200))
            popupWindow.open()
            return None

        # If the function did not return None, run the plotter function and save its output, which should be a path
        self.path = plotter.plotter(self.ticker.text , self.timeSpan.text)

        # If the output is actually the string 'stockError', there was a problem with the inputted ticker
        # Hence, show the corresponding pop-up window and return None
        if self.path == 'stockError':
            show = P3()
            popupWindow = Popup(title="Security Ticker Error", content=show, size_hint=(None, None), size=(500, 200))
            popupWindow.open()
            return None

        # If the path is the string 'dateError', some problem happened regarding the inputted timeSpan
        # Show the corresponding pop-up window and return None
        elif self.path == 'dateError':
            show = P2()
            popupWindow = Popup(title="Date Error", content=show, size_hint=(None, None), size=(1000, 200))
            popupWindow.open()
            return None

        # If no error was found, return the path
        return self.path


# Define the second screen's class
class SecondScreen(Screen):
    # Define a method that updates the path of the image found in the second screen with a given path
    def update_image_source(self, path):
        self.ids.image_display.source = path


class ModelingInp(Screen):
    # Create objects to store the ticker and the horizon
    ticker = ObjectProperty(None)
    horizon = ObjectProperty(None)

    # Function to model
    def submit(self):
        self.preds_path = None
        x = 0
        if not self.ticker.text or not self.horizon.text:
            return None
        print(self.ticker.text , self.horizon.text)

        patternTicker = r'(\^[A-Z]{3}C?)|^[A-Z]{3}(\.[A-Z])?$|^[A-Z]{4}$'
        if not bool(re.match(patternTicker, self.ticker.text)):
            print("Invalid ticker")
            self.ticker.text = ''
            x+=1
        try:
            h = int(self.horizon.text)
            if h < 0:
                h = h * -1
            elif h == 0:
                x+=1
                self.horizon.text = ''
        except:
            print("Invalid horizon")
            x+=1
            self.horizon.text = ''

        if x:
            show = P()
            popupWindow = Popup(title="Format Error", content=show, size_hint=(None, None), size=(700,200))
            popupWindow.open()
            return None

        self.preds_path = modelling.a_arima(security=self.ticker.text , h=h)

        if self.preds_path == 'stockError':
            show = P3()
            popupWindow = Popup(title="Security Ticker Error", content=show, size_hint=(None, None), size=(500, 200))
            popupWindow.open()
            self.preds_path = None
            return None

        return self.preds_path


class Predicted(Screen):
    def update_image_source(self , path):
        self.ids.image_display.source = path


class Return(Screen):
    # Define the global variables of ticker and timeSpan
    # These are initially empty, but will be filled by the user's input
    ticker = ObjectProperty(None)
    timeSpan = ObjectProperty(None)

    # Define the submit method that will be ran once the user press the submit button
    def submit(self):
        # The variable x will serve as a checking tool to see if everything is good
        x=0

        # Print the user's input texts
        print(self.ticker.text, self.timeSpan.text)

        # Check that the ticker inputted by the user matches any of the needed patterns:
        # 'MMMM' , 'MMM' , 'MMM.M' , '^MMM' , '^MMMM'
        # If the inputted ticker does not match, erase the input of the user and sum one to x
        patternTicker = r'(\^[A-Z]{3}C?)|^[A-Z]{3}(\.[A-Z])?$|^[A-Z]{4}$'
        if not bool(re.match(patternTicker, self.ticker.text)):
            print("Invalid ticker")
            self.ticker.text = ''
            x+=1

        # Check that the timeSpan matches the required pattern:
        # yyyy-mm-dd,yyyy-mm-dd
        # Where mm is a number such that (1<=mm<=12) and dd is a number such that (1<=dd<=31)
        # If the inputted timeSpan does not match, erase the input and sum one to x
        patternTime = r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01]),\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$'
        if not bool(re.match(patternTime, self.timeSpan.text)):
            print("Invalid Time Span")
            self.timeSpan.text = ''
            x+=1

        # If x is different from zero, some input was not manageable
        # Hence, show the first pop-up window with title 'Format Error'
        # Return None
        if x != 0:
            show = P()
            popupWindow = Popup(title="Format Error", content=show, size_hint=(None, None), size=(700,200))
            popupWindow.open()
            return None

        # If the function did not return None, run the plotter function and save its output, which should be a path
        self.secReturn = str(returnCalc.returnCalc(self.ticker.text , self.timeSpan.text))

        # If the output is actually the string 'stockError', there was a problem with the inputted ticker
        # Hence, show the corresponding pop-up window and return None
        if self.secReturn == 'stockError':
            show = P3()
            popupWindow = Popup(title="Security Ticker Error", content=show, size_hint=(None, None), size=(500, 200))
            popupWindow.open()
            return None

        # If the path is the string 'dateError', some problem happened regarding the inputted timeSpan
        # Show the corresponding pop-up window and return None
        elif self.secReturn == 'dateError':
            show = P2()
            popupWindow = Popup(title="Date Error", content=show, size_hint=(None, None), size=(1000, 200))
            popupWindow.open()
            return None

        show = PReturn(secReturn=self.secReturn , sec=self.ticker.text)
        popupWindow = Popup(title="Security Return", content=show, size_hint=(None, None), size=(600, 250))
        popupWindow.open()

        return self.secReturn



# Define the window manager's class
# All its logic will be managed in the .kv file
class WindowManager(ScreenManager):
    pass


# Define the builder of the app with the name of the .kv file
kv = Builder.load_file('my.kv')


# Define the app class
class MyApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    MyApp().run()