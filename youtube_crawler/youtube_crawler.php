#!/usr/bin/php
<?php

$baseUrl = 'https://www.googleapis.com/youtube/v3/';
$apiKey = 'AIzaSyC9qkuVGtbLoMWRBTXm23L0_N8OKpcF9rQ';
$channelId = 'UCnv6T5lLfRxvbUk-lzGC4XQ';
$out_file = 'out.txt';

$url = $baseUrl .'channels?' .
    'id=' . $channelId .
    '&part=contentDetails' . 
    '&key=' . $apiKey;
$json = json_decode(file_get_contents($url), true);
 
$playlist = $json['items'][0]['contentDetails']['relatedPlaylists']['uploads'];
 
$url = $baseUrl .'playlistItems?' .
 'part=snippet' .
 '&maxResults=50' .
 '&playlistId=' . $playlist .
 '&order=date' .
 '&key=' . $apiKey;
$json = json_decode(file_get_contents($url), true);
 
$videos = array();
foreach($json['items'] as $video)
    $videos[] = "http://www.youtube.com/watch?v=".$video['snippet']['resourceId']['videoId'];
 
while(isset($json['nextPageToken'])){
    $nextUrl = $url . '&pageToken=' . $json['nextPageToken'];
    $json = json_decode(file_get_contents($nextUrl), true);
    foreach($json['items'] as $video)
        $videos[] = "http://www.youtube.com/watch?v=".$video['snippet']['resourceId']['videoId'];
}

$videos = array_unique($videos);

$out_text = "";
foreach($videos as $video) {
    $out_text .= trim($video)."\n";
}

file_put_contents($out_file, $out_text);
