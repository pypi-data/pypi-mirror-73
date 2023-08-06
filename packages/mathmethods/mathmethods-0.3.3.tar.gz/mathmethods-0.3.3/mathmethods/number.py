import logging
logging.basicConfig(level=logging.INFO)

class Number:
    def __init__(self, num):
        self.num = num
        logging.info("Number initiated.")
        
    def get_number(self):
        print(f'Number is "{self.num}"')
        
    def squared(self):
        logging.info(f'Multiplying the squared variables of {self.num} is {self.num**2}')
        logging.debug(f'Square variable of {self.num} = {self.num**2}')
        return self.num**2
    
    def addition(self, additor):
        logging.debug(f'Number {self.num} + {additor}')
        return self.num+additor
    
    def substraction(self, substractor):
        logging.debug(f'Number {self.num} - {substractor}')
        return self.num-substractor
    
    def division(self, divider):
        return self.num/divider
    
    def is_even(self):
        if self.num % 2 == 0:
            logging.info(f"{self.num} is an even number")
            return True
        else:
            logging.info(f"{self.num} is an odd number")
            return False

