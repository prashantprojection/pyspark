import { Button, Table } from 'antd';
import React, { useState } from 'react';
import "./utils.css"

export default function BookListTable(props){
    const [selectedRowKeys, setSelectedRowKeys] = useState([]);
    const [loading, setLoading] = useState(false);

    const columns = props.columns;
    const readBook = props.readBook;
    const setReadBook = props.setReadBook;

    const start = () => {
        setLoading(true);
        // ajax request after empty completing
        setTimeout(() => {
          var newBooks = [];
          var count = 0;
          var flag = false;
          for(let i=0; i<readBook.length; i++){
            for(let j=0; j<selectedRowKeys.length; j++){
              if(selectedRowKeys[j] == readBook[i].key){
                flag = true;
                break;
              }
            }
            if(flag==false){
              newBooks.push({
                title: readBook[i].title,
                id: readBook[i].id,
                genres: readBook[i].genres,
                author: readBook[i].author,
                publisher: readBook[i].publisher,
                key: count
              });
              count++;
            }
            else{
              flag = false;
            }
          }
          console.log("newBook list: ",newBooks);
          setSelectedRowKeys([]);
          setLoading(false);
          setReadBook(newBooks);
        }, 500);
      };
      const onSelectChange = (newSelectedRowKeys) => {
        console.log('selectedRowKeys changed: ', newSelectedRowKeys);
        setSelectedRowKeys(newSelectedRowKeys);
      };
      const rowSelection = {
        selectedRowKeys,
        onChange: onSelectChange,
      };
      const hasSelected = selectedRowKeys.length > 0;
      return (
        <div>
          <div
            // style={{
            //   marginBottom: 16,
            // }}
          >
            {/* <div className='searchBtn'> */}
              <Button type="primary" onClick={()=>start(selectedRowKeys)} disabled={!hasSelected} loading={loading}>
              Remove from list
              </Button>
            {/* </div> */}
            <span
              style={{
                marginLeft: 8,
              }}
            >
              {hasSelected ? `Selected ${selectedRowKeys.length} items` : ''}
            </span>
          </div>
          <Table 
            rowSelection={rowSelection}
            columns={columns}
            dataSource={readBook}
            pagination={{pageSize:5}}
            size="small"
          />
        </div>
      );
}