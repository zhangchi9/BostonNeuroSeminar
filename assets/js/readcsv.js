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
     for(var cell_count=0; cell_count<=cell_data.length-1; cell_count++)
     {
      if (count === 0) 
      {
        if (cell_count===0) { table_data += '<tr>'}
        table_data += '<td>'+cell_data[cell_count]+'</td>';
        if (cell_count===(cell_data.length-1)) { table_data += '</tr>'}
      } 
      else 
      {
        var x = new Date(cell_data[0]);
        if (+x >= +today) {
          if (cell_count===0) { table_data += '<tr>'}
          table_data += '<td>'+cell_data[cell_count]+'</td>';
          if (cell_count===(cell_data.length-1)) { table_data += '</tr>'}
       } 
       else {
           break;
       } ;

      }
     }
    }

    table_data += '</table>';
    $('#talks_table').html(table_data);
    
   }
  });
 
});