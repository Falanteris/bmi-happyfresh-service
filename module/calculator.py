

class BMICalculator():
    def __init__(self,weight, height) -> None:
        """
        Initiate variables:

        Weight must be in "Kg"

        Height must be in "cm"
        """
        self.weight = weight
        self.height = height
    def calculate(self):
        """
        Calculate based on formula : kg/m2

        Height will be converted to meters first
        """
        self.bmi = round(float(self.weight / (self.height/100) ** 2),ndigits=1)
        
        return self
    def check(self):
        self.label = "healthy"
        
        if self.bmi < 18.5:
            self.label = "underweight"
        
        if self.bmi > 24.9:
            self.label = "overweight"
        
        return {
            "bmi": self.bmi,
            "label": self.label
        }
    


        
    

if __name__ == "__main__":
    print("Running Basic Debug Test for BMI Calculator")
    print(BMICalculator(90,170).calculate().check()) # overweight
    print(BMICalculator(60,170).calculate().check()) # normal/healthy
    print(BMICalculator(20,170).calculate().check()) # underweight
