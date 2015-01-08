def html_movie(plotfiles, interval_ms=300, width=800, height=600,casename='movie'):
    import os
    if not isinstance(plotfiles, (tuple,list)):
        raise TypeError('html_movie: plotfiles=%s of wrong type %s' %
                        (str(plotfiles), type(plotfiles)))
    # Check that the plot files really exist
    missing_files = [fname for fname in plotfiles if not os.path.isfile(fname)]
    if missing_files:
        raise ValueError('Missing plot files: %s' % str(missing_files)[1:-1])

    ext = os.path.splitext(plotfiles[0])[-1]
    if ext == '.png' or ext == '.jpg' or ext == '.jpeg' or ext == 'gif':
        pass
    else:
        raise ValueError('Plotfiles (%s, ...) must be PNG files with '\
                         'extension .png' % plotfiles[0])
        
    header = """\
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width" />
</head>
<style type="text/css">
    body { 
       margin: 10; 
       padding: 10
     }
    input{
       font-family:  Georgia, serif;
       font-size: 1em; /* 20px / 10px */
       color: #000 ;
       background-color: #ffb200 ;    
       border: 2px outset #b37d00 ;
       border-radius: 10px;
       width: 60px ;
       text-decoration: none ;
       background-color: #9cf ;
       border-top: 1px solid #c0ffff ;
       border-right: 1px solid #00f ;
       border-bottom: 1px solid #00f ;
       border-left: 1px solid #c0ffff ;
    }
    .push-down{
       border: 1px solid #38538c;
       background-color: #9cf;
       //color: #FFFFFF;
       text-shadow: 0px -1px 1px #213052;
       box-shadow: inset 0 1px 10px 1px #5D88E3, 0px 1px 0 #1C2C4D, 0 6px 0px #1D3054, 0px 10px 25px rgba(0,0,0,.7);
    }
    .push-down:hover{
       background: transparent;
       box-shadow: inset 0 0px 20px 1px #88ADFC, 0px 1px 0 #1C2C4D, 0 6px 0px #1D3054, 0px 10px 25px rgba(0,0,0,.7);
    }
    .push-down:active{
       box-shadow: inset 0 1px 10px 1px #5B89EB, 0 1px 0 #1A2847, 0 2px 0 #1C2D4D, 0px 3px 6px rgba(0,0,0,.9);
       margin-top: 10px;
    } 
</style> 
<body>
<div align="center">
"""
    no_images = len(plotfiles)
    jscode = """
<script language="Javascript">
<!---
var num_images_%(casename)s = %(no_images)d;
var img_width = %(width)d;
var img_height = %(height)d;
var interval = %(interval_ms)d;
var images_%(casename)s = new Array();

function preload_images_%(casename)s()
{
   t = document.getElementById("progress");
""" % vars()

    i = 0
    for fname in plotfiles:
        jscode += """
   t.innerHTML = "Preloading image ";
   images_%(casename)s[%(i)s] = new Image(img_width, img_height);
   images_%(casename)s[%(i)s].src = "%(fname)s";
        """ % vars()
        i = i+1
    jscode += """
   t.innerHTML = "";
}

function tick_%(casename)s()
{
   if (frame_%(casename)s > num_images_%(casename)s - 1)
       frame_%(casename)s = 0;

   document.movie.src = images_%(casename)s[frame_%(casename)s].src;
   frame_%(casename)s += 1;
   tt = setTimeout("tick_%(casename)s()", interval);
}

function startup_tmpmovie()
{
   preload_images_%(casename)s();
   frame_%(casename)s = 0;
   setTimeout("tick_%(casename)s()", interval);
}

function stopit()
{ clearTimeout(tt); }

function restart_tmpmovie()
{ tt = setTimeout("tick_%(casename)s()", interval); }

function slower()
{ interval = interval/0.7; }

function faster()
{ interval = interval*0.7; }

// --->
</script>
""" % vars()
    plotfile0 = plotfiles[0]
    form = """
<form>
&nbsp;
<input type="button" class="push-down" value="Play" onClick="startup_tmpmovie()">
<input type="button" class="push-down" value="Pause" onClick="stopit()">
<input type="button" class="push-down" value="Replay" onClick="restart_tmpmovie()">
&nbsp;
<input type="button" class="push-down" value="Slower" onClick="slower()">
<input type="button" class="push-down" value="Faster" onClick="faster()">
</form>

<p><div ID="progress"></div></p>
<img src="%(plotfile0)s" name="movie" border=2/></div>
""" % vars()
    footer = '\n</body>\n</html>\n'
    #print(footer)
    return header, jscode, form, footer

def movieHTML(files, interval_ms=300, width=800, height=600,output='movie'):
    import os,glob,re
    
    if isinstance(files, str):
       files = glob.glob(files)
       files.sort()
    print('Found %d files' ) %(len(files))
    message1='\nMaking HTML code for displaying'
    message2=''.join(files) 
    print(message1+message2)
    fps = 25;
    interval_ms = 1000.0/fps
    
    #if output is None:
    #   output = 'test'   
    
    header, jscode, form, footer = html_movie(files, interval_ms, casename=output)
    casename = os.path.splitext(output)[0] + '.html'
    
    f = open(casename, 'w')
    f.write(header + jscode + form + footer)
    f.close()
    print('\nmovie in output file %s') %casename
    return
    