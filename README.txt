Multitwitch -- Multiple twitch streams on one page.

Originally from https://github.com/bhamrick/multitwitch and used with
permission

### X3L Version of Multitwitch

### Creating the config file
The config file looks like this and must be in the runtime directory of the
project.

[DEFAULT]
community_name = x3lgaming  # any community name will work
title = X3LGaming Multitwitch  # the title used on the pages
base_url = http://some.url

[twitch]
apiurl = https://api.twitch.tv/kraken  # api url if needed to updated
follow_apiurl = https://api.twitch.tv/kraken/streams/followed  # same
# unauthclient is the app that gets community info and stream list
unauthclient_id = secret   # client id from app
# authclient is the app that gets follows; it needs user_read scope
authclient_id = secret   # client id from app
authclient_oath = secretoauth  # oauth token from app



unauthclient_id and authclient_id do not need to be the same. authclient_oauth
needs to come from the correct clientid though.

### How to get a client id
1. Create app here: https://dev.twitch.tv/dashboard/apps
2. Set the OAuth redirect URI to:
    https://twitchapps.com/tokengen/
3. Copy the client id afterwards


### How to get an oauth token
1. Make the client as above and copy the client id
2. Go to https://twitchapps.com/tokengen/ and enter client id
3. Enter the scopes required (likely user_read)
4. Click 'connect with twitch' and agree to the user popup
5. Copy the oauth and keep it secret

The user that is used in step 4 will be the user who's follows/etc is used by
the app.
