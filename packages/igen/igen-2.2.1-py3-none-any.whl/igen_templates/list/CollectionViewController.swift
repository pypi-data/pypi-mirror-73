import UIKit
import Reusable

final class {{ name }}ViewController: UIViewController, BindableType {

    // MARK: - IBOutlets

    @IBOutlet weak var collectionView: LoadMoreCollectionView!

    // MARK: - Properties

    var viewModel: {{ name }}ViewModel!

    struct LayoutOptions {
        var itemSpacing: CGFloat = 16
        var lineSpacing: CGFloat = 16
        var itemsPerRow: Int = 2

        var sectionInsets = UIEdgeInsets(
            top: 16.0,
            left: 16.0,
            bottom: 16.0,
            right: 16.0
        )

        var itemSize: CGSize {
            let screenSize = UIScreen.main.bounds

            let paddingSpace = sectionInsets.left
                + sectionInsets.right
                + CGFloat(itemsPerRow - 1) * itemSpacing

            let availableWidth = screenSize.width - paddingSpace
            let widthPerItem = availableWidth / CGFloat(itemsPerRow)
            let heightPerItem = widthPerItem

            return CGSize(width: widthPerItem, height: heightPerItem)
        }
    }

    private var layoutOptions = LayoutOptions()

    // MARK: - Life Cycle

    override func viewDidLoad() {
        super.viewDidLoad()
        configView()
    }

    deinit {
        logDeinit()
    }

    // MARK: - Methods

    private func configView() {
        collectionView.do {
            $0.register(cellType: {{ model_name }}Cell.self)
            $0.alwaysBounceVertical = true
            {% if not paging %}
            $0.refreshFooter = nil
            {% endif %}
        }

        collectionView.rx
            .setDelegate(self)
            .disposed(by: rx.disposeBag)
    }

    func bindViewModel() {
        let input = {{ name }}ViewModel.Input(
            loadTrigger: Driver.just(()),
            reloadTrigger: collectionView.refreshTrigger,
            {% if paging %}
            loadMoreTrigger: collectionView.loadMoreTrigger,
            {% endif %}
            select{{ model_name }}Trigger: collectionView.rx.itemSelected.asDriver()
        )

        let output = viewModel.transform(input)

        output.{{ model_variable }}List
            .drive(collectionView.rx.items) { collectionView, index, {{ model_variable }} in
                return collectionView.dequeueReusableCell(
                    for: IndexPath(row: index, section: 0),
                    cellType: {{ model_name }}Cell.self)
                    .then {
                        $0.bindViewModel({{ model_variable }})
                    }
            }
            .disposed(by: rx.disposeBag)

        output.error
            .drive(rx.error)
            .disposed(by: rx.disposeBag)

        output.isLoading
            .drive(rx.isLoading)
            .disposed(by: rx.disposeBag)

        output.isReloading
            .drive(collectionView.isRefreshing)
            .disposed(by: rx.disposeBag)

        {% if paging %}
        output.isLoadingMore
            .drive(collectionView.isLoadingMore)
            .disposed(by: rx.disposeBag)

        {% endif %}
        output.selected{{ model_name }}
            .drive()
            .disposed(by: rx.disposeBag)

        output.isEmpty
            .drive()
            .disposed(by: rx.disposeBag)
    }

}

// MARK: - Binders
extension {{ name }}ViewController {

}

// MARK: - UICollectionViewDelegate
extension {{ name }}ViewController: UICollectionViewDelegate, UICollectionViewDelegateFlowLayout {
    func collectionView(_ collectionView: UICollectionView,
                        layout collectionViewLayout: UICollectionViewLayout,
                        sizeForItemAt indexPath: IndexPath) -> CGSize {
        return layoutOptions.itemSize
    }

    func collectionView(_ collectionView: UICollectionView,
                        layout collectionViewLayout: UICollectionViewLayout,
                        insetForSectionAt section: Int) -> UIEdgeInsets {
        return layoutOptions.sectionInsets
    }

    func collectionView(_ collectionView: UICollectionView,
                        layout collectionViewLayout: UICollectionViewLayout,
                        minimumLineSpacingForSectionAt section: Int) -> CGFloat {
        return layoutOptions.lineSpacing
    }

    func collectionView(_ collectionView: UICollectionView,
                        layout collectionViewLayout: UICollectionViewLayout,
                        minimumInteritemSpacingForSectionAt section: Int) -> CGFloat {
        return layoutOptions.itemSpacing
    }
}

// MARK: - StoryboardSceneBased
extension {{ name }}ViewController: StoryboardSceneBased {
    static var sceneStoryboard = UIStoryboard()
}
