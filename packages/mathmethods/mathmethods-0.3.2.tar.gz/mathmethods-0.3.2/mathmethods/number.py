import logging
logging.basicConfig(level=logging.INFO)

class Number:
    def __init__(self, num):
        self.num = num
        logging.info("Student initiated.")
        
    def get_number(self):
        print(f'Number is "{self.num}"')
        
    def squared(self):
        logging.info(f'Multiplying the squared variables of {self.num} is {self.num**2}')
        logging.debug(f'Square variable of {self.num} = {self.num**2}')
        return self**2
    
    def addition(self, addition):
        logging.debug(f'Number {self.num} + {addition}')
        return self+addition
    
    def substraction(self, substraction):
        logging.debug(f'Number {self.num} - {substraction}')
        return self.num-substraction
    
    def division(self, divider):
        return self.num/divider

