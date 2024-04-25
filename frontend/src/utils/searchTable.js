import { Button, Table } from 'antd';
import React, { useState } from 'react';
import "./utils.css"

export default function SearchTable(props){
    const [selectedRowKeys, setSelectedRowKeys] = useState([]);
    const [loading, setLoading] = useState(false);

    const columns = props.columns;
    const data = props.data;
    const readBook = props.readBook;
    const setReadBook = props.setReadBook;
    // console.log(typeof(columns));
    // console.log(typeof(readBook));
    // console.log(typeof(setReadBook));

      const start = () => {
        setLoading(true);
        // ajax request after empty completing
        setTimeout(() => {
          var newBooks = [];
          for(let i=0; i<readBook.length; i++){
            newBooks.push(readBook[i]);
          }
          var count = readBook.length;
          for(let i=0; i<selectedRowKeys.length; i++){
            newBooks.push({
              title: data[selectedRowKeys[i]].title,
              id: data[selectedRowKeys[i]].id,
              genres: data[selectedRowKeys[i]].genres,
              rating: data[selectedRowKeys[i]].rating,
              pages: data[selectedRowKeys[i]].pages,
              author: data[selectedRowKeys[i]].author,
              publisher: data[selectedRowKeys[i]].publisher,
              key: count
            });
            count++;
          }
          console.log("newBooks: ",newBooks);
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
              Add to your read list
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
            dataSource={data}
            pagination={{pageSize:5}}
            size="small"
          />
        </div>
      );
}