import { Cell, Avatar } from '@vkontakte/vkui';
import { Icon12Circle } from '@vkontakte/icons';
export function MailItem({ keyEl, el, clickStatus }) {
  return (
    <>
      <Cell
        onStart={() => {
          clickStatus(keyEl)
        }}
        mode="selectable"
        before={
          <>
             <div style={{position: 'absolute', top: '10px', left: '5px', color: '#2688eb'}}>{el?.read === false ? (
              <Icon12Circle  style={{margin: 'auto', marginRight: '0px'}} />
              ) : (
                ""
              )}
            </div>
            <Avatar src={el?.author?.avatar} />
          </>}
        after={
          <div style={{ width: '100px', textAlign: 'right'}}>
            <div>{el?.dateTime}</div>
          </div>
        }
      >
        <>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
            <div>{el?.author?.name}</div>
            <img height={20} src={el?.file?.preview} />
          </div>
            <div style={{ color: '#aaaaaa' }}>{el?.title}</div>
            <div style={{ color: 'grey' }}>{el?.text}</div>
        </>
      </Cell>
    </>
  );
}
