<!DOCTYPE html>

<html>
	<head>
		<title>TEST</title>
		<link rel="stylesheet" text="type/css" href="style.css">
		<link rel="stylesheet" type="text/css" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css">
	</head>

	<body>
			<div id="header">
				<center>
					<h1>Sync an Account</h1>
				</center>
			</div>

			<div id="stripe">
				
			</div>

			<div id="content_wrapper">
				<div id="content_left">
					<nav>
						<ul>
							<li><a href="contact.html">Contact</a>
						</ul>
					</nav>
				</div>
				<div id="content_right" class="home">
						<div class="group">
							<br><br>
								<div id="logo">
									<img src="img/chase-logo-tran.png" id="logo">
								</div>
						</div>
							<form action="linked.html">
							  <div class="group">
								    <input type="text" required>
								    <span class="highlight"></span>
								    <span class="bar"></span>
							  		<label>Username</label>
							  </div>

							  <div class="group">  
								    <input type="password" required>
								    <span class="highlight"></span>
								    <span class="bar"></span>
								    <label>Password</label>

							  </div>
							  <div class="group" disabled>  
							 	<button id="credentialsCTA_before" class="btn btn-primary" type="button" onclick="showLoadingState()" disabled>Connect Account
								</button>
								<button id="credentialsCTA_after" class="btn btn-primary" type="button" value="Connect Account" disabled>
								  <span class="spinner-border spinner-border-sm" role="status"></span>
								  Loading...
								</button>
							</div>
							$(document).ready(function() {
							    $("#btnFetch").click(function() {
							      // disable button
							      $(this).prop("disabled", true);
							      // add spinner to button
							      $(this).html(
							        `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...`
							      );
							    });
							});
							<div style="margin:3em;">
									<form class="form-inline" id="topicForm" action="" method="POST">
									    <input type="text" id="inputTopic" name="topic" class="form-control mb-2 mr-sm-2" placeholder="Topic of interest" required autofocus/>
									    <button type="button" id="btnFetch" class="btn btn-primary mb-2">Submit</button>
									  </form>
							</div>

							</form>

				</div>
			</div>

		<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js"></script>
		<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js"></script>

	</body>
</html>

