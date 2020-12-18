A simple api authentication using firebase authentication and firebase admin sdk.

Frontend:

Authenticate an user and store the uid and idtoken given by the firebase authentication api

      var user;
      var appVerifier = new firebase.auth.RecaptchaVerifier('recaptcha-container', {
            'size': 'invisible',
            'callback': function(response) {

            },
            'expired-callback': function() {

            }
          });
      let context = this;
      firebase.auth().signInWithPhoneNumber('+91'+phoneNumber, appVerifier).then(function (confirmationResult) {
            confirmationResult.confirm(code).then(function (result) {  //code->otp received by the user
              // User signed in successfully.
              user = result.user;
              firebase.auth().currentUser.getIdToken(true).then(function(idToken) {
                     context.apiService.createUser(context.user.uid,idToken).subscribe((data) => console.log(data)); //API call for creating user
                     //Store the idtoken instead of passing as a parameter
                    });
            }).catch(function (error) {
              // User couldn't sign in (bad verification code?)
              console.log(error);
              alert("Incorrect OTP");
            });
      }).catch(function (error) {
          console.log(error);
      });


The API call createUser(uid,idToken) is given an idtoken and a firebase uid as header and sent to backend

Backend:

Receives idtoken and uid through createuser request and is verified using firebase admin sdk.
we use a decorator function to authenticate the user

      def token_required(f):
          @wraps(f)
          def decorated(*args,**kwargs):
              data = json.loads(request.data)
              token = data['idtoken'] //Token received from request
              try:
                  decoded_token = auth.verify_id_token(token)   //Verifies client given token and obtains a FirebaseToken object
                  if(data['uid'] == decoded_token['uid']): //Client uid is compared with the one obtained from FirebaseToken object
                      pass
                  else:
                      return 'authfailed'
              except firebase_admin.auth.InvalidIdTokenError:
                  return 'authfailed'
              return f(*args, **kwargs)
          return decorated

Replace firebase-admin-sdk-service.json with your project config.
      {
        "type": "service_account",
        "project_id": "x-xxxxx-xxxxx",
        "private_key_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "private_key": "-----BEGIN PRIVATE KEY-----\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n",
        "client_email": "firebase-adminsdk-xxxxxx@xxxxxxxxxxx.iam.gserviceaccount.com",
        "client_id": "xxxxxxxxxxxxxxxxxxx",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xxxxxx%xxxxxxxxxxxxxx.iam.gserviceaccount.com"
      }
