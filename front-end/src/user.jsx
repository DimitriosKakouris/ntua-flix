// import React from "react";
// import { useState, useEffect } from 'react';
// import ListGroup from './ListGroup';

// function User() {
//     const [data, setData] = useState([]);
//     const [city, setCity] = useState('');
//     const [count, setCount] = useState(0);
    
//     useEffect(() => {
//         fetch('/user')
//         .then((res) => res.json())
//         .then(apiData => {
//             setData(apiData);
            
//             // If you need to set city from the fetched data, 
//             // ensure the data structure supports it. For instance, 
//             // if apiData is an array and city is its second element:
            
//         })
//     }, []);

//  console.log(data);
//  console.log(count);

//  return (
//    <div className="App">
//      <header className="App-header">
//          <ListGroup >{data}</ListGroup>
//      </header>
//    </div>
//  );
// }

// export default User;