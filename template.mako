<html>
<!DOCTYPE html>
<%!
    from utils import sluggify
    from filters import legends, classes, special_char as special
%>
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<title>My Little Pony Visualized</title>
	<link href='https://fonts.googleapis.com/css?family=Lato:400,400italic,300,700' rel='stylesheet' type='text/css'>
	<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="container">
	<header class='main'>
		<h1>Visual Transcript of My Little Pony: Friendship is Magic</h1>
		<p>Each square represents a word, spoken or sung in the episode. 
			Data taken from the <a href="http://mlp.wikia.com/wiki/My_Little_Pony_Friendship_is_Magic_Wiki">Friendship is Magic Wiki</a></p>
	</header>
	<nav>
        % for season in seasons:
        <a href="#${ season.name | sluggify }">${ season.name | h }</a>
        % endfor
	</nav>
	<main>
        % for season in seasons:
		<h2 id="${ season.name | sluggify }">${ season.name | h }</h2>
		<div class="season" data-transcript="${ season.code }">
			% for episode in season.episodes:
			<div>
				<% lines = episode.lines.filter(lambda l: not l.is_action()) %>
				<div class="meta">
					<h3>${ episode.title | h }</h3>
					<p>${ str(len(lines)) } lines <br> ${ lines.wc } words</p>

                    % if episode.title in special:
                    <ul class="special">
                        % for name, classname in special[episode.title].items():
                            <li><span class="${ classname }"></span> ${ name | h }</li>
                        % endfor
                    </ul>
                    % endif
				</div>
				<ol class="lines">
					% for line in lines:
<li class="${ line.classname() }">${ 'a' * line.wc }</li>\
					% endfor
				</ol>
			</div>
			% endfor
		</div>
		% endfor
	</main>
	<aside class="legend">
        %for title, chars in legends:
        <h2>${ title | h }</h2>
        <ul>
            %for char in chars:
                <li><span class="${ classes[char] }"></span> ${ char | h}</li>
            %endfor
        </ul>
        %endfor

        <h2>Others</h2>
		<ul>
			<li><span class="so"></span>Songs</li>
			<li><span class="a"></span>Antagonist</li>
		</ul>

		<p class="instructions">Click on the legend above to filter</p>
	</aside>
	<footer></footer>

	<div class="line-info">
		<p class="speaker"></p>
		<p class="line"></p>
	</div>
	<div class="progress">Loading full transcript: <strong>0/6</strong></div>
</div>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
<script src="master.js"></script>
</body>
</html>