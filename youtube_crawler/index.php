<?php

// Call set_include_path() as needed to point to your client library.
require_once 'google-api-php-client/src/Google_Client.php';
require_once 'google-api-php-client/src/contrib/Google_YouTubeService.php';
session_start();

/* You can acquire an OAuth 2 ID/secret pair from the API Access tab on the Google APIs Console
 <http://code.google.com/apis/console#access>
For more information about using OAuth2 to access Google APIs, please visit:
<https://developers.google.com/accounts/docs/OAuth2>
Please ensure that you have enabled the YouTube Data API for your project. */
$OAUTH2_CLIENT_ID = '253367390360-0q720p00jjv8v1vs5e79lin5adpc87bg.apps.googleusercontent.com';
$OAUTH2_CLIENT_SECRET = '1UcUeReetq34ixK3BMsbLIha';

$client = new Google_Client();
$client->setClientId($OAUTH2_CLIENT_ID);
$client->setClientSecret($OAUTH2_CLIENT_SECRET);
$redirect = filter_var('http://' . $_SERVER['HTTP_HOST'] . $_SERVER['PHP_SELF'], FILTER_SANITIZE_URL);
$client->setRedirectUri($redirect);

// YouTube object used to make all API requests.
$youtube = new Google_YoutubeService($client);

if (isset($_GET['code'])) {
  if (strval($_SESSION['state']) !== strval($_GET['state'])) {
    die('The session state did not match.');
  }

  $client->authenticate();
  $_SESSION['token'] = $client->getAccessToken();
  header('Location: ' . $redirect);
}

if (isset($_GET['logout'])) {
    session_unset();
    $_SESSION = array();
    header('Location: ' . $redirect);
}


if (isset($_SESSION['token'])) {
  $client->setAccessToken($_SESSION['token']);
}

// Check if access token successfully acquired
if ($client->getAccessToken()) {

    if (!isset($_POST["url"])) {
      $htmlBody = "<form method='post'>
          URL: <input type='text' size='100' name='url' id='url' value='UCnv6T5lLfRxvbUk-lzGC4XQ'><br/><br/>
          <button type='submit'>Copy Videos to List</button>
        </form>";
        $htmlBody .= '<br/><br/><a href="http://'.$_SERVER['HTTP_HOST']. $_SERVER['PHP_SELF'].'?logout=yes">Logout</a>';
        
    }
    else {
        
      try {

            $plID = $_POST["url"];
            $options = array ("channelId" => $plID, "maxResults" => 50, "order" => "date");
            $listDetails = $youtube->search->listSearch("snippet", $options);
            $videos = array();
            
            if ( $listDetails["pageInfo"]["totalResults"] > 0 ) {

                do {

                    $list = $youtube->search->listSearch("snippet", $options);
                    $nextPageToken = $list["nextPageToken"];
                    $options["pageToken"] = $nextPageToken;
                    
                    //var_dump($list['pageInfo']['totalResults']."::".$list['pageInfo']['resultsPerPage']);

                    foreach ($list["items"] as $listItem) {
                        if( ($listItem["id"]["videoId"] != "") && ($listItem["id"]["videoId"] != NULL) ) {
                            //var_dump($listItem["id"]["videoId"]);
                            $videos[] =  "http://www.youtube.com/watch?v=".$listItem["id"]["videoId"];
                        }
                    }

                } while ($nextPageToken);

            }
        
        $videos = array_unique($videos);
        
        $out_text = "";
        foreach($videos as $video) {
            $out_text .= trim($video)."\n";
        }
        $file = 'out.txt';
        file_put_contents($file, $out_text);
        $htmlBody .= '<br/><br/><a href="http://'.$_SERVER['HTTP_HOST']. $_SERVER['REQUEST_URI'].'">Back</a>';
        $htmlBody .= '<br/><br/><a href="http://'.$_SERVER['HTTP_HOST']. $_SERVER['PHP_SELF'].'?logout=yes">Logout</a>';

      } catch (Google_ServiceException $e) {
        $htmlBody .= sprintf('<p>A service error occurred: <code>%s</code></p>',
            htmlspecialchars($e->getMessage()));
      } catch (Google_Exception $e) {
        $htmlBody .= sprintf('<p>An client error occurred: <code>%s</code></p>',
            htmlspecialchars($e->getMessage()));
      }

      $_SESSION['token'] = $client->getAccessToken();
    }

} else {
  // If the user hasn't authorized the app, initiate the OAuth flow
  $state = mt_rand();
  $client->setState($state);
  $_SESSION['state'] = $state;

  $authUrl = $client->createAuthUrl();

  $htmlBody =
  <<<END
  <h3>Authorization Required</h3>
  <p>You need to <a href="$authUrl">authorize access</a> before proceeding.<p>
END;
}
?>

<!doctype html>
<html>
<head>
<title>New Playlist</title>
</head>
<body>
  <?=$htmlBody?>
</body>
</html>
