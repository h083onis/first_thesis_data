import numpy as np
import matplotlib.pyplot as plt
import torch
from torcheval.metrics.functional import multiclass_auroc

# 損失計算用
def eval_loss(loader, device, net, criterion):
    
    # データローダーから最初の1セットを取得する
    for images, labels in loader:
        break

    # デバイスの割り当て
    inputs = images.to(device)
    labels = labels.to(device)

    # 予測計算
    outputs = net(inputs)

    #  損失計算
    loss = criterion(outputs, labels)

    return loss

# 学習用関数
def fit(net, optimizer, criterion, num_epochs, train_loader, test_loader, device, history, test_dataset):
    
    # tqdmライブラリのインポート
    from tqdm.notebook import tqdm

    base_epochs = len(history)
    
    inputs_auc_test = np.zeros((0,2000), dtype=np.int64)
    inputs_auc_test = torch.tensor(inputs_auc_test, dtype=torch.int64)
    labels_auc_test = np.zeros(0, dtype=np.int64)
    labels_auc_test = torch.tensor(labels_auc_test, dtype=torch.int64)
    
    for data, label in test_dataset:
        inputs_auc_test = torch.vstack((inputs_auc_test, data))
        labels_auc_test = torch.hstack((labels_auc_test, label))
  
    for epoch in range(base_epochs, num_epochs+base_epochs):
        # 1エポックあたりの正解数(精度計算用)
        n_train_acc, n_val_acc = 0, 0
        # 1エポックあたりの累積損失(平均化前)
        train_loss, val_loss = 0, 0
        # 1エポックあたりのデータ累積件数
        n_train, n_test = 0, 0
       
        # print(device)
        #訓練フェーズ
        net.train()

        for inputs, labels in tqdm(train_loader):
            # 1バッチあたりのデータ件数
            train_batch_size = len(labels)
            # 1エポックあたりのデータ累積件数
            n_train += train_batch_size
    
            # GPUヘ転送
            inputs = inputs.to(device)
            labels = labels.to(device)

            # 勾配の初期化
            optimizer.zero_grad()

            # 予測計算
            outputs = net(inputs)

            # 損失計算
            loss = criterion(outputs, labels)

            # 勾配計算
            loss.backward()

            # パラメータ修正
            optimizer.step()

            # 予測ラベル導出
            predicted = torch.max(outputs, 1)[1]

            # 平均前の損失と正解数の計算
            # lossは平均計算が行われているので平均前の損失に戻して加算
            train_loss += loss.item() * train_batch_size 
            n_train_acc += (predicted == labels).sum().item() 
            # print(n_train_acc / n_train)
        
        #予測フェーズ
        net.eval()
        with torch.no_grad():
            for inputs_test, labels_test in test_loader:
                # 1バッチあたりのデータ件数
                test_batch_size = len(labels_test)
                # 1エポックあたりのデータ累積件数
                n_test += test_batch_size

                # GPUヘ転送
                inputs_test = inputs_test.to(device)
                labels_test = labels_test.to(device)

                # 予測計算
                outputs_test = net(inputs_test)

                # 損失計算
                loss_test = criterion(outputs_test, labels_test)

                # 予測ラベル導出
                predicted_test = torch.max(outputs_test, 1)[1]

                #  平均前の損失と正解数の計算
                # lossは平均計算が行われているので平均前の損失に戻して加算
                val_loss +=  loss_test.item() * test_batch_size
                n_val_acc +=  (predicted_test == labels_test).sum().item()
                # print(n_val_acc, n_test)
                # print(cal_auc(outputs_test, labels_test))
            
        # 精度計算
        # print(n_train_acc, n_train)
        # print(n_val_acc, n_test)
        train_acc = n_train_acc / n_train
        val_acc = n_val_acc / n_test
        # 損失計算
        avg_train_loss = train_loss / n_train
        avg_val_loss = val_loss / n_test
        #AUC
        auc_score = cal_auc(net, inputs_auc_test, labels_auc_test, device)
        
        # 結果表示
        print (f'Epoch [{(epoch+1)}/{num_epochs+base_epochs}], loss: {avg_train_loss:.5f} acc: {train_acc:.5f} val_loss: {avg_val_loss:.5f}, val_acc: {val_acc:.5f}, auc_score: {auc_score:.5f}')
        # 記録
        item = np.array([epoch+1, avg_train_loss, train_acc, avg_val_loss, val_acc, auc_score])
        history = np.vstack((history, item))

    return history


def evaluate_history(history):
    #損失と精度の確認
    print(f'初期状態: 損失: {history[0,3]:.5f} 精度: {history[0,4]:.5f}') 
    print(f'最終状態: 損失: {history[-1,3]:.5f} 精度: {history[-1,4]:.5f}' )

    num_epochs = len(history)
    unit = num_epochs / 10

    # 学習曲線の表示 (損失)
    plt.figure(figsize=(9,8))
    plt.plot(history[:,0], history[:,1], 'b', label='訓練')
    plt.plot(history[:,0], history[:,3], 'k', label='検証')
    plt.xticks(np.arange(0,num_epochs+1, unit))
    plt.xlabel('繰り返し回数')
    plt.ylabel('損失')
    plt.title('学習曲線(損失)')
    plt.legend()
    plt.show()

    # 学習曲線の表示 (精度)
    plt.figure(figsize=(9,8))
    plt.plot(history[:,0], history[:,2], 'b', label='訓練')
    plt.plot(history[:,0], history[:,4], 'k', label='検証')
    plt.xticks(np.arange(0,num_epochs+1,unit))
    plt.xlabel('繰り返し回数')
    plt.ylabel('精度')
    plt.title('学習曲線(精度)')
    plt.legend()
    plt.show()
    
    plt.figure(figsize=(9,8))
    plt.plot(history[:,0], history[:,5], 'r', label='検証')
    plt.xticks(np.arange(0,num_epochs+1,unit))
    plt.xlabel('繰り返し回数')
    plt.ylabel('AUC')
    plt.title('学習曲線(AUC)')
    plt.legend()
    plt.show()
    

def cal_auc(net, inputs_auc_test, labels_auc_test, device):
    
    class_cnt = len(torch.unique(labels_auc_test))
    with torch.no_grad():
        inputs_auc_test = inputs_auc_test.to(device)
        labels_auc_test = labels_auc_test.to(device)
        outputs_test = net(inputs_auc_test)
        auc = multiclass_auroc(
            input = outputs_test,
            target = labels_auc_test,
            num_classes = class_cnt,
            average="macro"
        ).item()
    
    return auc
