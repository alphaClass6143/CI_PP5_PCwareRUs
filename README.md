# PCwareRUs

(Developer: Robin Bosch)

![PCwareRUs](docs/mockup.jpg)

[View live site](https://ci-pp5-pcwareurs.herokuapp.com/)

## Table of Content

1. [About](#about)
2. [Strategy](#strategy)
    1. [Site Owner Goals](#site-owner-goals)
    2. [User Goals](#user-goals)
    3. [Target Audience](#target-audience)
    4. [Business Model](#business-model)
    5. [SEO](#seo)
    6. [Marketing](#marketing)
3. [User Stories](#user-stories)
4. [Design](#design)
    1. [Design Choices](#design-choices)
    2. [Structure](#structure)
    3. [Database model](#database-model)
5. [Technologies Used](#technologies-used)
    1. [Languages](#languages)
    2. [Frameworks](#frameworks)
    3. [Python libraries](#python-libraries)
    4. [Tools](#tools)
6. [Features](#features)
7. [Validation and Testing](#validation-and-testing)
    1. [HTML Validation](#html-validation)
    2. [CSS Validation](#css-validation)
    3. [Accessibility](#accessibility)
    4. [Performance](#performance)
    5. [Device testing](#device-testing)
    6. [Browser compatibility](#browser-compatibility)
    7. [Testing user stories](#testing-user-stories)
8. [Bugs](#bugs)
9. [Deployment](#deployment)
10. [Credits](#credits)
    1. [Media](#media)
    2. [Code](#code)
    3. [Acknowledgements](#acknowledgements)
11. [License](#license)

## About

## Strategy

### Site Owner Goals

### User Goals

### Target Audience

### Business Model

### SEO

### Marketing

## User stories

## Design

### Design Choices

### Structure

### Database model

## Technologies Used

### Languages

- HTML  
- CSS
- Python
- JavaScript

### Frameworks

- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/icons)

### Python Libraries

django = "*"
stripe = "*"
pylint = "*"
boto3 = "*"
django-storages = "*"
pillow = "*"
psycopg2 = "*"
dj-database-url = "*"
load-dotenv = "*"
django-allauth = "*"
libsass = "*"
django-compressor = "*"
django-sass-processor = "*"
gunicorn = "*"
django-crispy-forms = "*"
django-countries = "*"

### Tools

- [Git](https://git-scm.com/)
- [GitHub](https://github.com/)
- [diagrams.net](https://www.diagrams.net/)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Balsamiq](https://balsamiq.com/)

## Features

## Validation and Testing

### HTML validation

### CSS validation

### Accessibility

### Performance

### Device testing

### Browser compatibility

### Testing user stories

## Bugs

|Status|Bug|Fix|
|---|---|---|
||||

## Deployment

1. Follow the clone steps below and go to step 2
2. Run the following command to install all required packages

```
pipenv install
```

3. Create a .env file and add the following keys to it:
    - STRIPE_SECRET_KEY --> Stripe secret key
    - STRIPE_PUBLIC_KEY --> Stripe public key
    - STRIPE_WH_SECRET --> Stripe webhook secret
    - AWS_ACCESS_KEY_ID --> The AWS access key
    - AWS_SECRET_ACCESS_KEY --> The AWS secret key
    - DATABASE_URL --> Your link to your postgres database
    - DEBUG --> Set either to True or False
    - EMAIL_HOST_USER --> Your email host (address)
    - EMAIL_HOST_PASS --> Your email password for programatic access
    - SECRET_KEY --> A random secret key, can be anything

4. Enter the following command to start up the server:

```
pipenv shell
cd pcwareurs
python3 manage.py runserver
```

5. The package can now be accessed locally under [localhost:8000](https://localhost:8000)
6. Don't forget to create a super user to access the admin panel with the following command:

```
python3 manage.py createsuperuser
```

Heroku:

1. Create an account at Heroku and login.
2. Click the "Create new app" button on your dashboard, add app name and region.
3. Click on the "Create app" button.
4. Click on the "Settings" tab.
5. Under "Config Vars" click "Reveal Config Vars" add the following keys:
    - STRIPE_SECRET_KEY --> Stripe secret key
    - STRIPE_PUBLIC_KEY --> Stripe public key
    - STRIPE_WH_SECRET --> Stripe webhook secret
    - AWS_ACCESS_KEY_ID --> The AWS access key
    - AWS_SECRET_ACCESS_KEY --> The AWS secret key
    - DATABASE_URL --> Your link to your postgres database
    - DEBUG --> Set either to True or False
    - EMAIL_HOST_USER --> Your email host (address)
    - EMAIL_HOST_PASS --> Your email password for programatic access
    - SECRET_KEY --> A random secret key, can be anything
6. Under "Buildpacks" click "Add buildpack" and then choose "Python" first and click "Save changes"
7. Go to the "Deploy" tab and choose GitHub as your deployment method
8. Connect your GitHub account
9. Enter your repository name, search for it and click connect when it appears below.
10. In the manual deploy section click "Deploy branch"
11. Optional: You can enable automatic deploys if you want the app to automatically update

You can fork the repository by following these steps:

1. Go to the repository on GitHub  
2. Click on the "Fork" button in the upper right hand corner

You can clone the repository by following these steps:

1. Go to the repository on GitHub
2. Locate the "Code" button above the list of files and click it  
3. Select if you prefer to clone using HTTPS, SSH, or Github CLI and click the "copy" button to copy the URL to your clipboard
4. Open Git Bash
5. Change the current working directory to the one where you want the cloned directory
6. Type git clone and paste the URL from the clipboard ($ git clone <https://github.com/YOUR-USERNAME/YOUR-REPOSITORY>)  
7. Press Enter to create your local clone.

## Credits

### Media

The following PC icon in the logo and icon was used
[PC Icon](https://www.flaticon.com/free-icon/computer-tower_9214538?term=pc&page=1&position=34&origin=tag&related_id=9214538)

The following banner was used on the social media and webpage
[Banner](https://www.freepik.com/free-vector/pc-computer-equipment-with-devices-accessories-flat-banner-set-isolated_2869541.htm#query=computer%20hardware%20banner&position=1&from_view=keyword)

Icons are taken from Font Awesome:  
[FontAwesome](<https://fontawesome.com/>)

Shop images are all taken from the price comparison site geizhals.de
[Website](https://geizhals.de/)

### Code

The Privacy Policy was generated by a generator
[Generator](https://www.privacypolicytemplate.net)

Terms and Conditions were generate by a generator
[Generator](https://www.termsandconditionsgenerator.com/)

Stripes quickstart was used for the payment element
[Quickstart](https://stripe.com/docs/payments/quickstart)

The stripe webhandler from the boutique ado repository was used
[Repository](https://github.com/ckz8780/boutique_ado_v1)

CSS Reset has been used in the reset.css file.  
It was written by Andy Bell in a blog post:  
[Blog post](<https://piccalil.li/blog/a-modern-css-reset/>)

Guides on Flexbox and Grid from CSS-Tricks, that have been used multiple times as a reference.  
[Complete Guide to Grid](<https://css-tricks.com/snippets/css/complete-guide-grid/>)  
[Complete Guide to Flexbox](<https://css-tricks.com/snippets/css/a-guide-to-flexbox/>)

### Acknowledgements

- A special thanks to my mentor Mo Shami for his feedback and advice, especially on the documentation.
- A thanks to the Code Institute for the great learning resources

## License

This project is published under the MIT license.  
[License](/LICENSE.txt)