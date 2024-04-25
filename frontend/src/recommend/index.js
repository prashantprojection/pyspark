import React, {useEffect, useState} from 'react'
import { Button, message } from "antd"
import { Link, useLocation } from 'react-router-dom'
import "./index.css"
import axios from "axios";
import API_URL from "../conf/api-url";


export function RecommendPage(){
    const [recResult, setRecResult] = useState([]);
    const location = useLocation();
    const GoogleLink = "https://www.google.com/search?q="
    console.log("location value: ",location.state)

    useEffect(()=>{
        axios
        .post(`${API_URL}/recommend`, location.state)
        .then((result)=>{
            console.log("received data:",result.data);
            setRecResult(result.data);
        })
        .catch((error)=>{
            console.error(error);
            message.error(error);
        });
    }, [])

    const gotoLike = (title)=>{
        window.location.href = `${GoogleLink}${title}`
    }

    if (recResult.length == 0){
        return( 
            <div id="loading">
                <Button
                    type="link"
                    loading="true"
                    size="large"
                    style={{fontSize:"250%"}}
                >
                    Looking for recommended books
                </Button>
            </div>
        )
    }
    else{
        return(
            <div>
                <h3>** Book Recommendation Results **</h3>
                <div id="book-list">
                    {recResult.map((book)=>{
                        if(book.rating!=null){
                        return(
                            <div className='book-card'>
                                <Link className='book-link' onClick={()=>gotoLike(book.title)}>
                                    <div>
                                        <img className='book-img' src={`${book.imgUrl}`}/>
                                    </div>
                                    <div className='book-contents'>
                                        <span className='book-title'>{book.title}</span>
                                        <span className='book-author'>author:  {book.author}</span>
                                        <span className='book-publisher'>publisher:  {book.publisher}</span>
                                        <span className='book-rating'>rating {book.rating}</span>
                                    </div>
                                </Link>
                            </div>
                        )
                        }
                        else{
                            return(
                                <div className='book-card'>
                                <Link className='book-link' onClick={gotoLike}>
                                    <div>
                                        <img className='book-img' src={`${book.imgUrl}`}/>
                                    </div>
                                    <div className='book-contents'>
                                        <span className='book-title'>{book.title}</span>
                                        <span className='book-author'>author:  {book.author}</span>
                                        <span className='book-publisher'>publisher:  {book.publisher}</span>
                                        <span className='book-rating'>rating -</span>
                                    </div>
                                </Link>
                            </div>
                            )
                        }
                    })}
                </div>

            </div>

        )
    }
}
