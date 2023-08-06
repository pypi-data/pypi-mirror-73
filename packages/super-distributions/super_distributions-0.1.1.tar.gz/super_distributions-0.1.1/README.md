Thanks for installing super_distributions!

It is a simple package for using some of the most popular distributions such as Gaussian & Binomial Distributions (more incoming)

#Setting it up

After you've installed the package, simply import the package with desired distrubution name like:

------->  from  super_distributions import Gaussian

You can then simply create an object for class Gaussian like:

------>   gaussian_one = Gaussian(mean_value, standard_deviation_value)   // Gaussian(20,3)
          gaussian_one.mean   // 20
          gaussian_one.stdev   // 3

Inbuilt functions for all distributions:   

object.read_data_file()

<!-- Function to read in data from a txt file. The txt file should have
one number (float) per line. The numbers are stored in the data attribute.
				
		Args:
			file_name (string): name of a file to read from
		
		Returns:
			None
		
		""" -->
        
        
object.calculate_mean() 
object.calculate_stdev()
object.pdf()
object.plot_histogram()
object.plot_histogram_pdf()



For any doubts, just write to me at narayansharma275@gmail.com or reach out to me on my LinkedIn - https://www.linkedin.com/in/narayansharma277/