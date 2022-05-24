const { spawn } = require('child_process');

module.exports = (app) => {
    app.get('/', (req, res)=>{
        res.render('index');
    });
    
    app.get('/search', (req, res)=>{
        const query = req.query;
        const question = query.question;
    
        // Tf-idf
    
        // const arr = [
        //     {
        //     title: 'asdassd',
        //     url: 'google.com',
        //     statement: "sum of the two element"
        // },
        //     {
        //     title: 'asdassd',
        //     url: 'google.com',
        //     statement: "sum of the two element"
        // },
        //     {
        //     title: 'asdassd',
        //     url: 'google.com',
        //     statement: "sum of the two element"
        // },
        //     {
        //     title: 'asdassd',
        //     url: 'google.com',
        //     statement: "sum of the two element"
        // },
        //     {
        //     title: 'asdassd',
        //     url: 'google.com',
        //     statement: "sum of the two element"
        // }
        // ];
        
        // console.log(typeof arr);
        // res.json(arr);

        var dataTosend;
        // var arr = [
        //     {
        //         title : {},
        //         url: {}
        //     }
        // ];
        var arr = [];
        const python = spawn('python', ['tf-idf.py', question]);
        python.stdout.on('data', (data)=>{
            console.log('Pipe data from python script...');
            dataTosend = data.toString();
            console.log(dataTosend);
            arr.push(dataTosend + '\n');
            // arr.title.push(dataTosend + '\n');
        });

        python.on('close', (code)=>{
            console.log(`child process close all stdio with code ${code}`);
            res.json(arr);
        });
    });
};