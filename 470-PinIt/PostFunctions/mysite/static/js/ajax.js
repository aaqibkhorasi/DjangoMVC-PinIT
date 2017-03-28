$(function(){
       $('a.up_vote').click(function(e) {
          e.preventDefault();
      
          var clickedItem = $(this);
          $.ajax({
            url: $(this).attr('href'),
            type :'get' ,
            success : function (data){
              // alert('success');
              console.log('hello from success ajax')
              $(clickedItem).siblings('p').html(data.count)
            },
            failure : function (data){
              alert('failure') ; 
            }
          }) ;  // ajax call 

       }); // upvote link call


       $('a.down_vote').click(function(e) {
          e.preventDefault();
          var clickedItem = $(this);
          $.ajax({
            url: $(this).attr('href'),
            type :'get' ,
            success : function (data){
              // alert('success');
              console.log('hello from success ajax')
              $(clickedItem).siblings('p').html(data.count)
            },
            failure : function (data){
              alert('failure') ; 
            }


          }) ;  // AJAX CALL 
        
       });  // DOWNVOTE LINK CALL 




    });