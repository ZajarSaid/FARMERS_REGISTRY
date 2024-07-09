from Production.models import Region, District
from django.shortcuts import get_object_or_404
from .models import Farm


def run():

 

  # retrieving all regions

  # regions = Region.objects.all()

  # for region in regions:
  #   print(f'{region.name}-{[district.name for district in region.districts.all()]}')


  # regional_ranks = (
  #       Farm.objects.values('owner', 'region')
  #       .annotate(total_output=Sum('total_output'))
  #       .order_by('-total_output')
  #   )

  # print(regional_ranks)

  

  



  

    
      

  

  

  




  

















    #description = 'For all kind of contracts'
    #Category.objects.create(name='Contracts', description= description)
    #g = Category.objects.values()
    # f_name = 'John'
    # m_name = 'John'
    # l_name = 'John'
    # age = 23
    #print (g)
    # User = Charithy.objects.create(first_name=f_name, middle_name=m_name, last_name=l_name, age=age)
    # Result = Charithy.objects.values().filter(age=25)
    
    # Result = Charithy.objects.all()
    # r2=Charithy.objects.select_related('created_by').values()
    # # Result.delete()
    # # print(Result)
    # for r in Result:
      
    #   print(r.created_by)
    # User.save()
    # Venues = Venue.objects.all()




        
        


  #  api_url = 'https://api.covid19api.com/countries'
   # response = requests.get(api_url)

   # if response.status_code == 200:
     #   if response.text:  # Check if response has data
      #      try:
       #         api_data = response.json()
        #        # Process the JSON data here
         #       for region in api_data:
          #          print (region)
           # except ValueError as e:
            #    print(f"Error parsing JSON: {e}")
        #else:
         #   print("Empty response received from the API.")
    #else:
     #   print(f"Failed to fetch data from API. Status code: {response.status_code}")




