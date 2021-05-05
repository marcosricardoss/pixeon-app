
# Pixeon Application  

### Running the Application  

The application is clustering using docker-compose needing only a few variables for its execution. These variables can come from the .env file, which should be located at the same level as the *docker-compose.yml* file, or indicate the file containing the environment variables through the *--env-file* option of the docker-compose: 

    docker-compose up -d (with the .env file in the same folder)

    docker-compose --env-file development.env up -d 

Sample variable files already ready to be used to run the application.  

### Documentation  

The application's API was specified using OpenAPI. This allowed us to add a Swagger service, where it is possible to see the API documentation, as well as providing the client where possible to make requests in the application.  

PS: If the specification file is not loaded, check the address for it in the field directed to the file in the *Swagger* panel.  

### Simulated Data  

With the application running, run the `bin/seed` command to populate the database with simulated data. At each execution of this command, random names for physicians and patients will be generated.  

### Defaul User  

When the application is started, it will create an API access user according to the values ​​of the variables APP_DEFAULT_USERNAME and APP_DEFAULT_PASS contained in the environment variables file.

In addition to being able to use the API itself to be able to create new users, you can also use `bin/adduser` for the same purpose:  

    bin/adduser <username>  <password>

### Testing

Run the application using *docker-compose-test.yml*:

    docker-compose -f docker-compose-test.yml up 
  
    or

    docker-compose -f docker-compose-test.yml --env-file development.env up

Then run the `bin/test` command. The automated tests will be performed using the coverage.py with the pytest library showing your results on the screen.