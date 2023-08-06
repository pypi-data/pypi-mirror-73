import random

class Guesser():
    """ Guesser that selects a random number between 0 and the limit indicated, and to which you can try to guess this number
    Attributes:
        guess (integer) representing the value selected to represent
        limit (integer) representing the limit value it can get
        
    Functions:
        make_guess(integer guess)
        reestart_guess(integer limit)
    """
    
    def __init__(self, limit=100):
        self.guess = random.randint(0, limit)
        self.limit = limit

    def make_guess(self, guess):
        """Function that responds to a guess.
        
        Args: 
            guess (integer): the guess made by the user

        Returns:
            string: indicates the distance to the correct guess
            boolean: indicates if the guess is correct or not
            
        """
        
        if guess > self.guess + self.limit/10 :
            return 'You are too high', False
        
        elif guess > self.guess :
            return 'You are a little high', False
        
        elif guess < self.guess - self.limit/10 :
            return 'You are too low', False
        
        elif guess< self.guess :
            return 'You are a little low', False
        
        elif guess == self.guess :
            return 'You are right', True
        
        else:
            return 'Something went wrong', False
        
    
    def get_correct_guess(self):
        
        """Function that return the number selected.
        
        Args: 
            None

        Returns:
            integer: indicates the number that was selected
        """
        
        return self.guess

    def reestart_guess(self, limit=100):
        
        """Function that selects another number as the guess.
        
        Args: 
            limit (integer) representing the limit value it can get

        Returns:
            None
        """
        self.guess = random.randint(0, limit)

