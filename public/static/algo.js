// $(document).ready(()=>{

//     $('form').on('submit', ()=>{
  
//         var item = $('form input');
//         var todo = {item: item.val()};
  
//         $.ajax({
//           type: 'post',
//           url: '/todo',
//           data: todo,
//           success: (data)=>{
//             //do something with the data via front-end framework
//             location.reload();
//           }
//         });
  
//         return false;
  
//     });
  
//     $('li').on('click', ()=>{
//         var item = $(this).text().replace(/ /g, "-");
//         $.ajax({
//           type: 'DELETE',
//           url: '/todo/' + item,
//           success: (data)=>{
//             //do something with the data via front-end framework
//             location.reload();
//           }
//         });
//     });
  
//   });
  