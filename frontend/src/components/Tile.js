import React from 'react';

export function Tile(props) {
  return (
    <div className='center'>
      <div className='File'>
        {props.child}
      </div>
    </div>
  );
}
