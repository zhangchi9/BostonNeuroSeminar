$(document).ready(function(){
  $.ajax({
   url:"https://zhangchi9.github.io/BostonNeuroSeminar/Talks.csv",
   dataType:"text",
   success:function(data)
   {
    var d = new Date();
    var month = d.getMonth()+1
    var day = d.getDate()
    var result = month.toString() +"/"+day.toString();
    var today = new Date(result);
    
    var employee_data = data.split(/\r?\n|\r/);
    var table_data = '<table class="table table-bordered table-striped">';

    for(var count = 0; count<=employee_data.length-2; count++)
    {
     var cell_data = employee_data[count].split("#");
     table_data += '<tr>';
     for(var cell_count=0; cell_count<=cell_data.length-1; cell_count++)
     {
      if(count === 0)
      {
       table_data += '<th>'+cell_data[cell_count]+'</th>';
      }
      else
      {
        var x = new Date(cell_data[0]);
        if (true) {
          if (+x === +today) {
            if (cell_count==0) {
              table_data += '<td>'+'Today'+'</td>';
            } else {
              table_data += '<td>'+cell_data[cell_count]+'</td>';
            }
          } else {
            table_data += '<td>'+cell_data[cell_count]+'</td>';
          }
       } 
       else {
           break;
       } ;
      }
     }
     table_data += '</tr>';
    }

    table_data += '</table>';
    $('#talks_table').html(table_data);
    
   }
  });
 
});