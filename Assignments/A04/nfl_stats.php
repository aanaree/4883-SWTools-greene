<?php
//Connect to mysql
$host = "cs2.mwsu.edu";             // because we are ON the server
$user = "software_tools";        // user name

// Get username and password from slack
// The DB username and pass not the ones
// I sent you to log into the server.
$password = "horseblanketdonkey";         // password 
$database = "nfl_data";              // database 
$mysqli = mysqli_connect($host, $user, $password, $database);

if (mysqli_connect_errno($mysqli)) {
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
}


/**
 * This function runs a SQL query and returns the data in an associative array
 * that looks like:
 * $response [
 *      "success" => true or false
 *      "error" => contains error if success == false
 *      "result" => associative array of the result
 * ]
 *
 */
function runQuery($mysqli,$sql){
    $response = [];

    // run the query
    $result = $mysqli->query($sql);

    // If we were successful
    if($result){
        $response['success'] = true;
        // loop through the result printing each row
        while($row = $result->fetch_assoc()){
            $response['result'][] = $row;
        }
        $result->free();
    }else{
        $response['success'] = false;
        $response['error'] = $mysqli->error;
    }

    return $response;
}

//Q1
$sql = "SELECT id, `name`, COUNT(DISTINCT club) as total_team
        FROM players
        GROUP BY `name`
        ORDER BY total_team DESC
        limit 10";

$response = runQuery($mysqli, $sql);

echo "<pre>";   // so whitespace matters

if($response['success'])
{
    $num=1;
    PRINT "Q1\nTeams Played For: \n\n";
    PRINT "#   \t PlayerID \t   Name \t# Team\n================================================\n";
    foreach($response['result'] as $row)
    {
        PRINT "$num  ";
        $num +=1;
        echo "\t{$row['id']} \t{$row['name']} \t  {$row['total_team']}\n";
    }
    PRINT "================================================\n";
}

//Q2
$sql = "SELECT playerid, players.name,players_stats.season, SUM(yards) as tyards
        FROM players_stats
        LEFT JOIN players on players_stats.playerid = players.id
        WHERE statid = '10'
        GROUP BY season, playerid,'name'
        ORDER BY tyards DESC, season limit 5";

$response = runQuery($mysqli, $sql);

echo "<pre>";   // so whitespace matters
   
if($response['success']){
    $num = 1;
    PRINT "Q2\nTop 5 Rushing Players: \n\n";
    PRINT "# PlayerID \t   Name \tYear \t # Yards\n=================================================\n";
    foreach($response['result'] as $row){
        PRINT "$num  ";
        $num +=1;
        echo "{$row['playerid']} \t{$row['name']} \t{$row['season']}\t {$row['tyards']}\n";   
    }
    PRINT "=================================================\n";
}

//Q3
$sql = "SELECT playerid, players.name,players_stats.season, SUM(yards) as tyards
        FROM players_stats
        LEFT JOIN players on players_stats.playerid = players.id
        WHERE statid = '10'
        GROUP BY season, playerid,'name'
        ORDER BY tyards ASC
        limit 5";

$response = runQuery($mysqli, $sql);

echo "<pre>";   // so whitespace matters


if($response['success']){
    $num = 1;
    PRINT "Q3\nBottom 5 Passing Players: \n\n";
    PRINT "# PlayerID \t   Name \tYear \t # Yards\n=================================================\n";
    foreach($response['result'] as $row){
        PRINT "$num  ";
        $num +=1;
        echo "{$row['playerid']} \t{$row['name']}   \t{$row['season']}\t {$row['tyards']}\n";
    }
    PRINT "=================================================\n";
}

//Q4
$sql = "SELECT players_stats.playerid, players.name, players_stats.season, sum(players_stats.yards) as tyards 
        FROM `players_stats` 
        JOIN players on players.id=players_stats.playerid 
        WHERE statid = 10 and yards <0 
        GROUP BY playerid 
        ORDER BY Yards ASC limit 5";

$response = runQuery($mysqli, $sql);

echo "<pre>";   // so whitespace matters


if($response['success']){
    $num = 1;
    PRINT "Q4\nTop 5 Players with most Rushes for a Loss: \n\n";
    PRINT "# PlayerID \t   Name \tYear \t # Yards\n=================================================\n";
    foreach($response['result'] as $row){
        PRINT "$num  ";
        $num +=1;
        echo "{$row['playerid']} \t{$row['name']}   \t{$row['season']}\t {$row['tyards']}\n";
    }
    PRINT "=================================================\n";
}
//Q5
$sql = "SELECT club, sum(pen) as tpen 
        FROM `game_totals` 
        GROUP BY club 
        ORDER BY tpen DESC limit 5";

$response = runQuery($mysqli, $sql);

echo "<pre>";   // so whitespace matters


if($response['success']){
    $num = 1;
    PRINT "Q5\nTop 5 Players with most Rushes for a Loss: \n\n";
    PRINT "# Team \t   Penalties\n===================\n";
    foreach($response['result'] as $row){
        PRINT "$num  ";
        $num +=1;
        echo "{$row['club']} \t     {$row['tpen']}\n";
    }
    PRINT "===================\n";
}

//Q5
$sql = "SELECT club,season, sum(pen) as tpen,AVG(pen) as avgpen
        FROM `game_totals` 
        GROUP BY season 
        ORDER BY season ASC";

$response = runQuery($mysqli, $sql);

echo "<pre>";   // so whitespace matters


if($response['success']){
    $num = 1;
    PRINT "Q6\nAverage Penalties per Year: \n\n";
    PRINT "#\tYear \tTotal Penalties   Average Penalties \n===============================================\n";
    foreach($response['result'] as $row){
        PRINT "$num  ";
        $num +=1;
        echo "\t{$row['season']} \t   {$row['tpen']} \t      {$row['avgpen']}\n";
    }
    PRINT "===============================================\n";
}


//Q6
$sql = "SELECT season,count(distinct(gameid)) As Games, count(playid) as Plays, clubid, (count(playid)/count(distinct(gameid))) As Average 
        FROM `plays` NATURAL JOIN games GROUP BY season, clubid ORDER BY Average limit 10";
$response = runQuery($mysqli, $sql);

echo "<pre>";   // so whitespace matters


if($response['success']){
    $num = 1;
    PRINT "Q7\n Least Average Plays per Year: \n\n";
    PRINT "#\tYear \tTeam   Average Plays \n=================================================\n";
    foreach($response['result'] as $row){
        PRINT "$num  ";
        $num +=1;
        echo "\t{$row['season']} \t\t  {$row['clubid']} \t\t {$row['Average']} \n";
    }
    PRINT "=================================================\n";
}

//Q7
$sql = "SELECT count(yards) as Yards, playerid , name,players_stats.season
        FROM `players_stats` join players on players.id=players_stats.playerid
         WHERE statid = 70 and yards > 40 
        group by playerid order by yards desc limit 5";
$response = runQuery($mysqli, $sql);

echo "<pre>";   // so whitespace matters


if($response['success']){
    $num = 1;
    PRINT "Q8\nTop 5 Players that had field goals over 40 Yards \n\n";
    PRINT "#\tPlayerID \tName\tSeason\tYards \n=================================================\n";
    foreach($response['result'] as $row){
        PRINT "$num  ";
        $num +=1;
        echo "\t{$row['playerid']}  \t{$row['name']}\t {$row['season']}\t   {$row['Yards']} \n";
    }
    PRINT "=================================================\n";
}

//Q8
$sql = "SELECT count(yards) as NumYards,  name,sum(yards) as SumYards, playerid , players_stats.season, (count(yards)/sum(yards)) as Average 
        FROM `players_stats` join players on players.id = players_stats.playerid WHERE statid = 70  
        group by playerid order by Average limit 5";
$response = runQuery($mysqli, $sql);

echo "<pre>";   // so whitespace matters


if($response['success']){
    $num = 1;
    PRINT "Q9\nTop 5 Players witht the shortest average field Goal\n\n";
    PRINT "#\tPlayerID \tName\t\tSeason\tAverage Yards \n=============================================================\n";
    foreach($response['result'] as $row){
        PRINT "$num  ";
        $num +=1;
        echo "\t{$row['playerid']}  \t{$row['name']}  \t{$row['season']}\t   {$row['Average']}\n";
    }
    PRINT "=============================================================\n";
}

//Q10
$sql = "SELECT home_club, (count(winner)/count(*)*100)as perct
        FROM games 
        GROUP BY home_club";
$response = runQuery($mysqli, $sql);

echo "<pre>";   // so whitespace matters

if($response['success']){
    $num = 32;
    PRINT "Q10\nRank the NFL by win loss percentage\n\n";
    PRINT "#\tTeam \tWin/Loss % \n============================\n";
    foreach($response['result'] as $row){
        PRINT "$num  ";
        $num -=1;
        echo "\t{$row['home_club']}  \t{$row['perct']}\n";
    }
    PRINT "=================================================\n";
}