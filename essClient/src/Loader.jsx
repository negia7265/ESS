const Loader=({loading})=>{
    const spinStyle={
    width:'100px',
    height:'100px',
    border: '10px solid #f3f3f3',
    borderRadius: '50%',
    borderTop: '10px solid #3498db',
    animation: 'spin .5s linear infinite',
    }
    const positionLoader={
      position:'absolute',
      top:'20%',
      left:'50%',
    }
    if(loading==true)
    return <div style={positionLoader}>
    <div style={spinStyle} ></div>
    <style jsx>{`
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }

    `}</style>
    </div>
    return <></>
    }
    export default Loader;