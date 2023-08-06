import logging
logging.basicConfig(level=logging.INFO)

class Number:
    def __init__(self, num):
        self.num = num
        logging.info("Student initiated.")
        
    def get_number(self):
        print(f'Number is "{self.num}"')
        
    def squared(self, num):
        logging.info(f'Multiplying the squared variables of {num} is {num**2}')
        logging.debug(f'Square variable of {num} = {num**2}')
        return num**2
    
    def addition(self, num, addition):
        logging.debug(f'Number {num} + {addition}')
        return num+addition
    
    def substraction(self, num, substraction):
        logging.debug(f'Number {num} - {substraction}')
        return num-substraction

