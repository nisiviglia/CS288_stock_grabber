<?php
$servername = "localhost";
$username = "CS288";
$password = "spring2017";
$dbname = "stock_market";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

//get table name 
$query_get_table_names = "SELECT table_name FROM information_schema.tables WHERE table_schema='" . $dbname . "' ORDER BY table_name DESC";
$table = $conn->query($query_get_table_names)->fetch_row()[0];

//get data from table
$stocks = array();
$query_get_data = "SELECT * FROM " . $table;
if($result = $conn->query($query_get_data)) {
    while($row = $result->fetch_row()) {
        $stocks[] = $row;
    }
}
?>

<html>
<head>
<title>HW9</title>
</head>
<body>
  <table border="1">
    <tr>
      <td><a>Number</a></td>
      <td><a>Name</a></td>
      <td><a>Symbol</a></td>
      <td><a>Volume</a></td>
      <td><a>Price</a></td>
      <td><a>Change</a></td>
      <td><a>Precent Change</a></td>
    </tr>
    <?php foreach($stocks as $stock): ?>
      <tr>
        <td><?php echo $stock[0]; ?></td>
        <td><?php echo $stock[1]; ?></td>
        <td><?php echo $stock[2]; ?></td>
        <td><?php echo $stock[3]; ?></td>
        <td><?php echo $stock[4]; ?></td>
        <td><?php echo $stock[5]; ?></td>
        <td><?php echo $stock[6]; ?></td>
      </tr>
    <?php endforeach; ?>
  </table>
</body>
</html>

