<?php

# Setting time and memory limits
ini_set('max_execution_time',0);
ini_set('memory_limit', '128M');

define('AC_DIR', dirname(__FILE__));

# Including classes
require_once( AC_DIR . DIRECTORY_SEPARATOR . 'classes' . DIRECTORY_SEPARATOR . 'RollingCurl.class.php');
require_once( AC_DIR . DIRECTORY_SEPARATOR . 'classes' . DIRECTORY_SEPARATOR . 'AngryCurl.class.php');

# Initializing AngryCurl instance with callback function named 'callback_function'
$AC = new AngryCurl('callback_function');

# Initializing so called 'web-console mode' with direct cosnole-like output
$AC->init_console();

$filename = "emails.txt";
$emails = file($filename, FILE_IGNORE_NEW_LINES);

# Basic request usage (for extended - see demo folder)
foreach ($emails as $email) {
    $url = "http://domw.net/data.php";
    $post_data = array('name' => 'email', 'cmd' => $email);
    $AC->post($url, $post_data);
}


# Starting with number of threads = 200
$AC->execute(200);

# You may pring debug information, if console_mode is NOT on ( $AC->init_console(); )
//AngryCurl::print_debug(); 

# Destroying
unset($AC);

# Callback function example
function callback_function($response, $info, $request)
{
    if($info['http_code']!==200)
    {
        AngryCurl::add_debug_msg(
            "->\t" .
            $request->options[CURLOPT_PROXY] .
            "\tFAILED\t" .
            $info['http_code'] .
            "\t" .
            $info['total_time'] .
            "\t" .
            $info['url']
        );
    }else
    {
        AngryCurl::add_debug_msg(
            "->\t" .
            $request->options[CURLOPT_PROXY] .
            "\tOK\t" .
            $info['http_code'] .
            "\t" .
            $info['total_time'] .
            "\t" .
            $info['url']
        );
        preg_match("/style='color:#008736'>Успешное соединение/", $response, $m);
        if(!empty($m)) {
            $data = $request->post_data['cmd'].':OK'.PHP_EOL;
        }
        else {
            $data = $request->post_data['cmd'].':FAIL'.PHP_EOL;
        }
        $fp = fopen('result.txt', 'a');
        fwrite($fp, $data);
    }
    
    return;
}
