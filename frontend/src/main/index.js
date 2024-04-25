import React from "react";
import {Link, useNavigate} from "react-router-dom";
import {Button} from "antd";
import "./index.css"
export function MainPage(){
    return(
        <div id="header">
            <p id="mainPageText">Book Recommendation Site</p>
            <div id="mainPageButton">
                <div class="mainButton">
                    <Link to="/foreign">
                        <Button type="primary" size="large">
                        Book Recommendation
                        </Button>
                    </Link>
                </div>
            </div>
        </div>
    );
}
